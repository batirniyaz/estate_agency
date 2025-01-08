import os
from typing import Optional, List

from fastapi import HTTPException, status, UploadFile, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.bot.handlers import send_message_to_channel
from app.config import CHANNEL_RENT_ID, CHANNEL_SALE_ID
from app.object.functions import generate_crm_id
from app.object.functions.validations.validate_media import validate_media
from app.object.messages import send_sale_comm, send_rent_comm
from app.object.models import CurrentStatus, ActionType
from app.object.models.commercial import CommercialMedia, Commercial
from app.object.schemas.commercial import CommercialCreate, CommercialResponse, CommercialUpdate
from app.utils.file_utils import save_upload_file

from app.object.functions.validations.validate_commercial import validate_commercial


async def create_commercial(
        current_user, db: AsyncSession,
        commercial: CommercialCreate,
        media: Optional[List[UploadFile]] = None,
        background_tasks: BackgroundTasks = None
):

    await validate_commercial(db, commercial)

    try:

        commercial.crm_id = await generate_crm_id(db, Commercial, 'C')
        commercial.responsible = current_user.full_name
        commercial.agent_commission = commercial.agent_percent * commercial.price / 100
        if commercial.second_responsible and commercial.second_agent_percent:
            commercial.second_agent_commission = commercial.second_agent_percent * commercial.price / 100

        if commercial.current_status == CurrentStatus.FREE:
            commercial.status_date = None

        db_commercial = Commercial(**commercial.model_dump())
        db.add(db_commercial)
        await db.commit()
        await db.refresh(db_commercial)

        if media:
            await validate_media(media)

            urls = save_upload_file(media, db_commercial.id, 'commercial')
            for url in urls:
                db_commercial_media = CommercialMedia(commercial_id=db_commercial.id, url=url['url'],
                                                      media_type=url['media_type'])
                db.add(db_commercial_media)
                db_commercial.media.append(db_commercial_media)

        await db.commit()
        await db.refresh(db_commercial)

        if db_commercial.action_type == ActionType.RENT:
            message = await send_rent_comm(db_commercial)
        else:
            message = await send_sale_comm(db_commercial, current_user.phone)

        background_tasks.add_task(send_message_to_channel, message, db_commercial.media,
                                  CHANNEL_RENT_ID if db_commercial.action_type == ActionType.RENT else CHANNEL_SALE_ID)

        commercial_response = CommercialResponse.model_validate(db_commercial)
        return jsonable_encoder(commercial_response)

    except IntegrityError as e:
        if 'duplicate key value violates unique constraint' in str(e):
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Коммерческий объект с таким номером уже существует")
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Произошла ошибка: {str(e)}")


async def get_commercials(db: AsyncSession, limit: int = 10, page: int = 1):
    try:
        total_count = await db.scalar(select(func.count(Commercial.id)))
        result = await db.execute(
            select(Commercial).order_by(Commercial.id.desc()).limit(limit).offset((page - 1) * limit))
        commercials = result.scalars().all()

        return {"data": commercials if commercials else [], "total_count": total_count}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_commercial(db: AsyncSession, commercial_id: int):
    result = await db.execute(select(Commercial).filter_by(id=commercial_id))
    commercial = result.scalars().first()
    if not commercial:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Коммерческий объект не найден")

    return commercial


async def update_commercial(
        db: AsyncSession,
        commercial_id: int,
        commercial: CommercialUpdate,
        user,
        media: Optional[List[UploadFile]] = None,
        background_tasks: BackgroundTasks = None
):

    db_commercial = await get_commercial(db, commercial_id)
    print(db_commercial)
    if not user.is_superuser and user.full_name != db_commercial.responsible:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Этот объект может изменить только ответственный")

    await validate_commercial(db, commercial)

    try:
        if commercial.agent_percent and commercial.price:
            commercial.agent_commission = commercial.agent_percent * commercial.price / 100

        if commercial.second_responsible and commercial.second_agent_percent and commercial.price:
            commercial.second_agent_commission = commercial.second_agent_percent * commercial.price / 100

        if commercial.current_status == CurrentStatus.FREE:
            commercial.status_date = None

        if media and len(media) > 0:
            if not media[0].filename == '':
                await validate_media(media)

                last_media = db_commercial.media[-1].url if db_commercial.media else None

                if last_media:
                    name, ext = last_media.rsplit('.', 1)

                urls = save_upload_file(media, db_commercial.id, 'commercial', name[-1] if last_media else None)
                for url in urls:
                    db_commercial_media = CommercialMedia(commercial_id=db_commercial.id, url=url['url'],
                                                          media_type=url['media_type'])
                    db.add(db_commercial_media)
                    db_commercial.media.append(db_commercial_media)

        for key, value in commercial.model_dump(exclude_unset=True).items():
            setattr(db_commercial, key, value)

        await db.commit()
        await db.refresh(db_commercial)

        commercial_response = CommercialResponse.model_validate(db_commercial)
        return jsonable_encoder(commercial_response)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def delete_commercial(db: AsyncSession, commercial_id: int):
    db_commercial = await get_commercial(db, commercial_id)

    try:
        for media in db_commercial.media:
            file_path = os.path.join("app/storage", "commercial", os.path.basename(media.url))
            if os.path.exists(file_path):
                os.remove(file_path)
            await db.delete(media)

        await db.delete(db_commercial)
        await db.commit()
        return {"detail": "Коммерческий объект удален"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
