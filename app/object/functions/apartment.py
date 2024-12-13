import os
from typing import Optional, List

from fastapi import HTTPException, status, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.object.functions import generate_crm_id
from app.object.functions.validations.validate_media import validate_media
from app.object.models.apartment import Apartment, ApartmentMedia
from app.object.schemas.apartment import ApartmentCreate, ApartmentUpdate, ApartmentResponse
from app.utils.file_utils import save_upload_file

from app.object.functions.validations.validate_apartment import validate_apartment


async def create_apartment(
        current_user, db: AsyncSession, apartment: ApartmentCreate, media: Optional[List[UploadFile]] = None):
    try:
        await validate_apartment(db, apartment)

        apartment.crm_id = await generate_crm_id(db, Apartment, 'A')
        apartment.responsible = current_user.full_name
        apartment.agent_commission = apartment.agent_percent * apartment.price / 100
        db_apartment = Apartment(**apartment.model_dump())
        db.add(db_apartment)
        await db.commit()
        await db.refresh(db_apartment)

        if media:
            await validate_media(media)

            urls = save_upload_file(media, db_apartment.id, 'apartment')
            for url in urls:
                db_apartment_media = ApartmentMedia(apartment_id=db_apartment.id, url=url['url'], media_type=url['media_type'])
                db.add(db_apartment_media)
                db_apartment.media.append(db_apartment_media)

        await db.commit()
        await db.refresh(db_apartment)

        apartment_response = ApartmentResponse.model_validate(db_apartment)
        return jsonable_encoder(apartment_response)

    except IntegrityError as e:
        if 'duplicate key value violates unique constraint' in str(e):
            print(e)
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Apartment already exists")
        raise
    pass


async def get_apartments(db: AsyncSession, limit: int = 10, page: int = 1):
    result = await db.execute(select(Apartment).limit(limit).offset((page - 1) * limit))
    apartment = result.scalars().all()

    return apartment if apartment else []
    pass


async def get_apartment(db: AsyncSession, apartment_id: int):
    result = await db.execute(select(Apartment).filter_by(id=apartment_id))
    apartment = result.scalars().first()
    if not apartment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Apartment not found")

    return apartment
    pass


async def update_apartment(
        db: AsyncSession,
        apartment_id: int,
        apartment: ApartmentUpdate,
        agent_name: str,
        media: Optional[List[UploadFile]] = None
):
    db_apartment = await get_apartment(db, apartment_id)
    if agent_name != db_apartment.responsible:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='This object created by another agent')

    try:
        await validate_apartment(db, apartment)

        apartment.agent_commission = apartment.agent_percent * apartment.price / 100

        if media:
            await validate_media(media)

            last_media = db_apartment.media[-1].url if db_apartment.media else None
            name, ext = last_media.split('.')

            urls = save_upload_file(media, db_apartment.id, 'apartment', name[-1])
            for url in urls:
                db_apartment_media = ApartmentMedia(apartment_id=db_apartment.id, url=url['url'],
                                                    media_type=url['media_type'])
                db.add(db_apartment_media)
                db_apartment.media.append(db_apartment_media)

        for key, value in apartment.model_dump(exclude_unset=True).items():
            setattr(db_apartment, key, value)

        await db.commit()
        await db.refresh(db_apartment)

        return db_apartment

    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def delete_apartment(db: AsyncSession, apartment_id: int, agent_name: str):
    try:
        db_apartment = await get_apartment(db, apartment_id)

        if agent_name != db_apartment.responsible:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You are not allowed to delete this commercial")

        for media in db_apartment.media:
            file_path = os.path.join("app/storage", "apartment", os.path.basename(media.url))
            if os.path.exists(file_path):
                os.remove(file_path)
            await db.delete(media)

        await db.delete(db_apartment)
        await db.commit()
        return {"detail": "Apartment deleted"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
