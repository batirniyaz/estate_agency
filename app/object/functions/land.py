import os
from typing import Optional, List

from fastapi import HTTPException, status, UploadFile, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.bot.handlers import send_message_to_channel
from app.object.functions import generate_crm_id, house_condition_translation
from app.object.functions.validations.validate_media import validate_media
from app.object.models import CurrentStatus
from app.object.models.land import LandMedia, Land
from app.object.schemas.land import LandCreate, LandResponse, LandUpdate
from app.utils.file_utils import save_upload_file

from app.object.functions.validations.validate_land import validate_land


async def create_land(
        current_user, db: AsyncSession, land: LandCreate,
        media: Optional[List[UploadFile]] = None,
        background_tasks: BackgroundTasks = None,
):

    await validate_land(db, land)

    try:

        land.crm_id = await generate_crm_id(db, Land, 'L')
        land.responsible = current_user.full_name
        land.agent_commission = land.agent_percent * land.price / 100
        if land.second_responsible and land.second_agent_percent:
            land.second_agent_commission = land.second_agent_percent * land.price / 100

        if land.current_status == CurrentStatus.FREE:
            land.status_date = None

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

        message = (f'<b>Сдаётся шикарный участок🏡</b>\n\n📍Район: {db_land.district}\n'
                                      f'📍Адрес: {db_land.title}\n\n'
                                      f'🎯{db_land.rooms} комн {db_land.floor_number}'
                                      f'\n🎯Площадь: {db_land.square_area} м²\n'
                                      f'🎯{house_condition_translation.get(db_land.house_condition.name)}✅\n'
                                      f'🎯Mебель {"✅" if db_land.furnished else "❌"}\n\n'
                                      f'❗Депозит: Договорная\n'
                                      f'❗Предоплата: Договорная\n'
                                      f'💰Цена: {db_land.price}$ есть торг\n'
                                      f'🌀Срм - {db_land.crm_id}\n\n'
                                      f'С уважением {db_land.responsible}\n'
                                      f'Специалист по недвижимости!\n'
                                      f'Имеется также более 10000 вариантов по всему городу.✅\n')

        background_tasks.add_task(send_message_to_channel, message, db_land.media)

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
    result = await db.execute(select(Land).filter_by(id=land_id))
    land = result.scalars().first()
    if not land:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Land not found")

    return land


async def update_land(
        db: AsyncSession,
        land_id: int,
        land: LandUpdate,
        user,
        media: Optional[List[UploadFile]] = None
):

    db_land = await get_land(db, land_id)
    if user.full_name != db_land.responsible and not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='This object created by another agent')

    if land.deal:
        if not user.is_superuser:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This commercial is busy. Not allowed to update')


    await validate_land(db, land)
    try:

        if land.agent_percent and land.price:
            land.agent_commission = land.agent_percent * land.price / 100
        if land.second_agent_percent and land.price and land.second_responsible:
            land.second_agent_commission = land.second_agent_percent * land.price / 100

        if land.current_status == CurrentStatus.FREE:
            land.status_date = None


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


async def delete_land(db: AsyncSession, land_id: int):
    db_land = await get_land(db, land_id)

    try:
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

