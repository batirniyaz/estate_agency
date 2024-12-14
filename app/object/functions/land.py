import os
from typing import Optional, List

from fastapi import HTTPException, status, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.bot.handlers import send_message_to_channel
from app.object.functions import generate_crm_id
from app.object.functions.validations.validate_media import validate_media
from app.object.models.land import LandMedia, Land
from app.object.schemas.land import LandCreate, LandResponse, LandUpdate
from app.utils.file_utils import save_upload_file

from app.object.functions.validations.validate_land import validate_land


async def create_land(
        current_user, db: AsyncSession, land: LandCreate, media: Optional[List[UploadFile]] = None):
    try:
        await validate_land(db, land)

        land.crm_id = await generate_crm_id(db, Land, 'L')
        land.responsible = current_user.full_name
        land.agent_commission = land.agent_percent * land.price / 100
        db_land = Land(**land.model_dump())
        db.add(db_land)
        await db.commit()
        await db.refresh(db_land)

        if media:
            await validate_media(media)

            urls = save_upload_file(media, db_land.id, 'land')
            for url in urls:
                db_land_media = LandMedia(land_id=db_land.id, url=url['url'], media_type=url['media_type'])
                db.add(db_land_media)
                db_land.media.append(db_land_media)

        await db.commit()
        await db.refresh(db_land)

        if land.description:
            await send_message_to_channel(f'<b>{db_land.title}</b>\n\n{db_land.description}\n\n{db_land.crm_id}')

        land_response = LandResponse.model_validate(db_land)
        return jsonable_encoder(land_response)

    except IntegrityError as e:
        if 'duplicate key value violates unique constraint' in str(e):
            print(e)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Land already exists")
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")


async def get_lands(db: AsyncSession, limit: int = 10, page: int = 1):
    try:
        total_count = await db.scalar(select(func.count(Land.id)))
        result = await db.execute(select(Land).order_by(Land.id.desc()).limit(limit).offset((page - 1) * limit))
        lands = result.scalars().all()

        return {"data": lands if lands else [], "total_count": total_count}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_land(db: AsyncSession, land_id: int):
    try:
        result = await db.execute(select(Land).filter_by(id=land_id))
        land = result.scalars().first()

        if not land:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Land not found")

        return land
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def update_land(
        db: AsyncSession,
        land_id: int,
        land: LandUpdate,
        agent_name,
        media: Optional[List[UploadFile]] = None
):
    try:
        db_land = await get_land(db, land_id)
        if agent_name != db_land.responsible:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='This object created by another agent')

        await validate_land(db, land)

        if land.agent_percent and land.price:
            land.agent_commission = land.agent_percent * land.price / 100

        if media and len(media) > 0:
            if not media[0].filename == '':
                await validate_media(media)

                last_media = db_land.media[-1].url if db_land.media else None
                if last_media:
                    name, ext = last_media.rsplit('.', 1)

                urls = save_upload_file(media, db_land.id, 'land', name[-1] if last_media else None)
                for url in urls:
                    db_land_media = LandMedia(land_id=db_land.id, url=url['url'], media_type=url['media_type'])
                    db.add(db_land_media)
                    db_land.media.append(db_land_media)

        for key, value in land.model_dump(exclude_unset=True).items():
            setattr(db_land, key, value)

        db.add(db_land)
        await db.commit()
        await db.refresh(db_land)

        land_response = LandResponse.model_validate(db_land)
        return jsonable_encoder(land_response)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def delete_land(db: AsyncSession, land_id: int, agent_name):
    try:
        db_land = await get_land(db, land_id)

        if agent_name != db_land.responsible:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='This object created by another agent')

        for media in db_land.media:
            file_path = os.path.join("app/storage", "land", os.path.basename(media.url))
            if os.path.exists(file_path):
                os.remove(file_path)
            await db.delete(media)

        await db.delete(db_land)
        await db.commit()
        return {"detail": "Land deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

