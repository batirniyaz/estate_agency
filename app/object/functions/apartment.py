import os

from fastapi import HTTPException, status, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.object.models.apartment import Apartment, ApartmentMedia
from app.object.schemas.apartment import ApartmentCreate, ApartmentUpdate, ApartmentResponse
from app.utils.file_utils import save_upload_file

from app.object.functions.validations.validate_apartment import validate_apartment


async def generate_crm_id(mapper, connection, target):
    async with AsyncSession(bind=connection) as session:
        res = await session.execute(select(Apartment).order_by(ApartmentMedia.id.desc()).limit(1))
        max_id = res.scalar()
        next_id = (max_id.id + 1) if max_id else 1
        target.crm_id = f"A{next_id}"


event.listen(Apartment, 'before_insert', generate_crm_id)


async def create_apartment(db: AsyncSession, apartment: ApartmentCreate, media: [UploadFile], current_user):
    try:
        apartment_validation = await validate_apartment(db, apartment)

        if apartment_validation:
            apartment.responsible = current_user.full_name
            apartment.agent_commission = apartment.agent_percent * apartment.price / 100
            db_apartment = Apartment(**apartment.model_dump())
            db.add(db_apartment)
            await db.commit()
            await db.refresh(db_apartment)

            urls = save_upload_file(media, db_apartment.id, 'apartment')
            for url in urls:
                db_apartment_media = ApartmentMedia(id=db_apartment.id, url=url['url'], media_type=url['media_type'])
                db.add(db_apartment_media)
                db_apartment.media.append(db_apartment_media)

            await db.commit()
            await db.refresh(db_apartment)

            apartment_response = ApartmentResponse.model_validate(db_apartment)
            return jsonable_encoder(apartment_response)
    except IntegrityError as e:
        if 'duplicate key value violates unique constraint' in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Apartment already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
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


async def update_apartment(db: AsyncSession, apartment_id: int, apartment: ApartmentUpdate):
    db_apartment = await get_apartment(db, apartment_id)

    try:

        apartment_validation = await validate_apartment(db, apartment)
        if apartment_validation:
            apartment.agent_commission = apartment.agent_percent * apartment.price / 100

            for key, value in apartment.model_dump(exclude_unset=True).items():
                setattr(db_apartment, key, value)

            await db.commit()
            await db.refresh(db_apartment)

            return db_apartment

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def delete_apartment(db: AsyncSession, apartment_id: int):
    db_apartment = await get_apartment(db, apartment_id)
    for media in db_apartment.media:
        file_path = os.path.join("app/storage", "images" if media.media_type == 'image' else 'videos', os.path.basename(media.url))
        if os.path.exists(file_path):
            os.remove(file_path)
        await db.delete(media)

    await db.delete(db_apartment)
    await db.commit()
    return {"detail": "Apartment deleted"}
