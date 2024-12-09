import os

from fastapi import HTTPException, status, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.object.functions import generate_crm_id
from app.object.models.land import LandMedia, Land
from app.object.schemas.land import LandCreate, LandResponse, LandUpdate
from app.utils.file_utils import save_upload_file

from app.object.functions.validations.validate_land import validate_land


async def create_land(db: AsyncSession, land: LandCreate, media: [UploadFile], current_user):
    try:
        land_validation = await validate_land(db, land)

        if land_validation:
            land.crm_id = await generate_crm_id(db, Land, 'L')
            land.responsible = current_user.full_name
            land.agent_commission = land.agent_percent * land.price / 100
            db_land = Land(**land.model_dump())
            db.add(db_land)
            await db.commit()
            await db.refresh(db_land)

            urls = save_upload_file(media, db_land.id, 'land')
            for url in urls:
                db_land_media = LandMedia(land_id=db_land.id, url=url['url'], media_type=url['media_type'])
                db.add(db_land_media)
                db_land.media.append(db_land_media)

            await db.commit()
            await db.refresh(db_land)

            land_response = LandResponse.model_validate(db_land)
            return jsonable_encoder(land_response)
    except IntegrityError as e:
        if 'duplicate key value violates unique constraint' in str(e):
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Land already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def get_lands(db: AsyncSession, limit: int = 10, page: int = 1):
    try:
        result = await db.execute(select(Land).limit(limit).offset((page - 1) * limit))
        lands = result.scalars().all()

        return lands if lands else []
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


async def update_land(db: AsyncSession, land_id: int, land: LandUpdate, agent_name):
    try:
        db_land = await get_land(db, land_id)
        if agent_name != db_land.responsible:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='This object created by another agent')

        land_validation = await validate_land(db, land)
        if land_validation:
            land.agent_commission = land.agent_percent * land.price / 100

            for key, value in land.model_dump().items():
                setattr(db_land, key, value)

            db.add(db_land)
            await db.commit()
            await db.refresh(db_land)

            land_response = LandResponse.model_validate(db_land)
            return jsonable_encoder(land_response)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def delete_land(db: AsyncSession, land_id: int):
    try:
        db_land = await get_land(db, land_id)
        for media in db_land.media:
            file_path = os.path.join("app/storage", "land", os.path.basename(media.url))
            if os.path.exists(file_path):
                os.remove(file_path)
            await db.delete(media)

        await db.delete(db_land)
        await db.commit()
        return {"detail": "Land deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

