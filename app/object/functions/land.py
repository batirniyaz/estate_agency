import os

from fastapi import HTTPException, status, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.object.models.land import LandMedia, Land
from app.object.schemas.land import LandCreate, LandResponse, LandUpdate
from app.utils.file_utils import save_upload_file

from app.object.functions.validations.validate_land import validate_land


async def generate_crm_id(mapper, connection, target):
    async with AsyncSession(bind=connection) as session:
        res = await session.execute(select(Land).order_by(LandMedia.id.desc()).limit(1))
        max_id = res.scalar()
        next_id = (max_id.id + 1) if max_id else 1
        target.crm_id = f"L{next_id}"


event.listen(Land, 'before_insert', generate_crm_id)


async def create_land(db: AsyncSession, land: LandCreate, media: [UploadFile], current_user):
    try:
        land_validation = await validate_land(db, land)

        if land_validation:
            land.responsible = current_user.full_name
            land.agent_commission = land.agent_percent * land.price / 100
            db_land = Land(**land.model_dump())
            db.add(db_land)
            await db.commit()
            await db.refresh(db_land)

            urls = save_upload_file(media, db_land.id, 'land')
            for url in urls:
                db_land_media = LandMedia(id=db_land.id, url=url['url'], media_type=url['media_type'])
                db.add(db_land_media)
                db_land.media.append(db_land_media)

            await db.commit()
            await db.refresh(db_land)

            land_response = LandResponse.model_validate(db_land)
            return jsonable_encoder(land_response)
    except IntegrityError as e:
        if 'duplicate key value violates unique constraint' in str(e):
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


async def update_land(db: AsyncSession, land_id: int, land: LandUpdate):
    try:
        db_land = await get_land(db, land_id)

        land_validation = await validate_land(db, land)
        if land_validation:
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

        await db.delete(db_land)
        await db.commit()
        return {"detail": "Land deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
