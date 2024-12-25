import os
from typing import Optional, List

from fastapi import HTTPException, status, UploadFile, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.bot.handlers import send_message_to_channel
from app.object.functions import generate_crm_id
from app.object.functions.validations.validate_media import validate_media
from app.object.messages import send_rent_apart, send_sale_apart
from app.object.models import CurrentStatus
from app.object.models.apartment import Apartment, ApartmentMedia
from app.object.schemas.apartment import ApartmentCreate, ApartmentUpdate, ApartmentResponse
from app.report.deals.crud import create_deal
from app.utils.file_utils import save_upload_file

from app.object.functions.validations.validate_apartment import validate_apartment
from app.config import CHANNEL_RENT_ID, CHANNEL_SALE_ID


async def create_apartment(

        current_user, db: AsyncSession,
        apartment: ApartmentCreate,
        media: Optional[List[UploadFile]] = None,
        background_tasks: BackgroundTasks = None):

    await validate_apartment(db, apartment)

    try:

        apartment.crm_id = await generate_crm_id(db, Apartment, 'A')
        apartment.responsible = current_user.full_name
        apartment.agent_commission = apartment.agent_percent * apartment.price / 100
        if apartment.second_responsible and apartment.second_agent_percent:
            apartment.second_agent_commission = apartment.second_agent_percent * apartment.price / 100

        if apartment.current_status == CurrentStatus.FREE:
            apartment.status_date = None

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

        if db_apartment.action_type == 'rent':
            message = await send_rent_apart(db_apartment)
        else:
            message = await send_sale_apart(db_apartment, current_user.phone)

        background_tasks.add_task(send_message_to_channel, message, db_apartment.media,
                                  CHANNEL_RENT_ID if db_apartment.action_type == 'rent' else CHANNEL_SALE_ID)

        apartment_response = ApartmentResponse.model_validate(db_apartment)
        return jsonable_encoder(apartment_response)

    except IntegrityError as e:
        if 'duplicate key value violates unique constraint' in str(e):
            print(e)
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Квартира с таким номером уже существует")
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Произошла ошибка: {str(e)}")
    pass


async def get_apartments(db: AsyncSession, limit: int = 10, page: int = 1):
    total_count = await db.scalar(select(func.count(Apartment.id)))
    result = await db.execute(select(Apartment).order_by(Apartment.id.desc()).limit(limit).offset((page - 1) * limit))
    apartment = result.scalars().all()

    return {"data": apartment if apartment else [], "total_count": total_count}


async def get_apartment(db: AsyncSession, apartment_id: int):
    result = await db.execute(select(Apartment).filter_by(id=apartment_id))
    apartment = result.scalars().first()
    if not apartment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Квартира не найдена")

    return apartment


async def update_apartment(
        db: AsyncSession,
        apartment_id: int,
        apartment: ApartmentUpdate,
        user,
        media: Optional[List[UploadFile]] = None,
        background_tasks: BackgroundTasks = None
):

    db_apartment = await get_apartment(db, apartment_id)
    if not user.is_superuser and user.full_name != db_apartment.responsible:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Этот объект может изменить только ответственный')

    await validate_apartment(db, apartment)
    try:
        if apartment.agent_percent and apartment.price:
            apartment.agent_commission = apartment.agent_percent * apartment.price / 100

        if apartment.second_responsible and apartment.second_agent_percent and apartment.price:
            apartment.second_agent_commission = apartment.second_agent_percent * apartment.price / 100

        if apartment.current_status == CurrentStatus.FREE:
            apartment.status_date = None

        if media and len(media) > 0:
            if not media[0].filename == '':

                await validate_media(media)

                last_media = db_apartment.media[-1].url if db_apartment.media else None
                if last_media:
                    name, ext = last_media.rsplit('.', 1)

                urls = save_upload_file(media, db_apartment.id, 'apartment', name[-1] if last_media else None)
                for url in urls:
                    db_apartment_media = ApartmentMedia(apartment_id=db_apartment.id, url=url['url'],
                                                        media_type=url['media_type'])
                    db.add(db_apartment_media)
                    db_apartment.media.append(db_apartment_media)

        for key, value in apartment.model_dump(exclude_unset=True).items():
            setattr(db_apartment, key, value)

        await db.commit()
        await db.refresh(db_apartment)

        if apartment.deal:
            background_tasks.add_task(create_deal, db, db_apartment.action_type, db_apartment.responsible,
                                      db_apartment.updated_at.strftime('%Y-%m-%d'), db_apartment.crm_id, db_apartment.price,
                                      db_apartment.agent_commission, db_apartment.agent_percent)

        apartment_response = ApartmentResponse.model_validate(db_apartment)
        return jsonable_encoder(apartment_response)

    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def delete_apartment(db: AsyncSession, apartment_id: int):
    db_apartment = await get_apartment(db, apartment_id)

    try:
        for media in db_apartment.media:
            file_path = os.path.join("app/storage", "apartment", os.path.basename(media.url))
            if os.path.exists(file_path):
                os.remove(file_path)
            await db.delete(media)

        await db.delete(db_apartment)
        await db.commit()
        return {"detail": "Квартира удалена"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
