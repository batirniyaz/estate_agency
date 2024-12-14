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
from app.object.models.commercial import CommercialMedia, Commercial
from app.object.schemas.commercial import CommercialCreate, CommercialResponse, CommercialUpdate
from app.utils.file_utils import save_upload_file

from app.object.functions.validations.validate_commercial import validate_commercial


async def create_commercial(
        current_user, db: AsyncSession, commercial: CommercialCreate, media: Optional[List[UploadFile]] = None):
    try:
        await validate_commercial(db, commercial)

        commercial.crm_id = await generate_crm_id(db, Commercial, 'C')
        commercial.responsible = current_user.full_name
        commercial.agent_commission = commercial.agent_percent * commercial.price / 100
        db_commercial = Commercial(**commercial.model_dump())
        db.add(db_commercial)
        await db.commit()
        await db.refresh(db_commercial)

        if media:
            await validate_media(media)

            urls = save_upload_file(media, db_commercial.id, 'commercial')
            for url in urls:
                db_commercial_media = CommercialMedia(commercial_id=db_commercial.id, url=url['url'], media_type=url['media_type'])
                db.add(db_commercial_media)
                db_commercial.media.append(db_commercial_media)

        await db.commit()
        await db.refresh(db_commercial)

        if commercial.description:
            await send_message_to_channel(f'<b>{db_commercial.title}</b>\n\n{db_commercial.description}\n\n{db_commercial.crm_id}')

        commercial_response = CommercialResponse.model_validate(db_commercial)
        return jsonable_encoder(commercial_response)

    except IntegrityError as e:
        if 'duplicate key value violates unique constraint' in str(e):
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Commercial already exists")
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_commercials(db: AsyncSession, limit: int = 10, page: int = 1):
    try:
        total_count = await db.scalar(select(func.count(Commercial.id)))
        result = await db.execute(select(Commercial).limit(limit).offset((page - 1) * limit))
        commercials = result.scalars().all()

        return {"data": commercials if commercials else [], "total_count": total_count}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_commercial(db: AsyncSession, commercial_id: int):
    try:
        result = await db.execute(select(Commercial).filter_by(id=commercial_id))
        commercial = result.scalars().first()

        return commercial if commercial else []
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def update_commercial(
        db: AsyncSession,
        commercial_id: int,
        commercial: CommercialUpdate,
        agent_name,
        media: Optional[List[UploadFile]] = None
):
    try:
        db_commercial = await get_commercial(db, commercial_id)
        if agent_name != db_commercial.responsible:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this commercial")

        await validate_commercial(db, commercial)

        commercial.agent_commission = commercial.agent_percent * commercial.price / 100

        if media:
            await validate_media(media)

            last_media = db_commercial.media[-1].url if db_commercial.media else None
            name, ext = last_media.split('.')

            urls = save_upload_file(media, db_commercial.id, 'commercial', name[-1])
            for url in urls:
                db_commercial_media = CommercialMedia(commercial_id=db_commercial.id, url=url['url'], media_type=url['media_type'])
                db.add(db_commercial_media)
                db_commercial.media.append(db_commercial_media)

        for key, value in commercial.model_dump(exclude_unset=True).items():
            setattr(db_commercial, key, value)

        await db.commit()
        await db.refresh(db_commercial)

        return db_commercial
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def delete_commercial(db: AsyncSession, commercial_id: int, agent_name):
    try:
        db_commercial = await get_commercial(db, commercial_id)
        if agent_name != db_commercial.responsible:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this commercial")

        for media in db_commercial.media:
            file_path = os.path.join("app/storage", "commercial", os.path.basename(media.url))
            if os.path.exists(file_path):
                os.remove(file_path)
            await db.delete(media)

        await db.delete(db_commercial)
        await db.commit()
        return {"detail": "Commercial deleted"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
