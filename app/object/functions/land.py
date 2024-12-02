from fastapi import HTTPException, status, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.object.models.land import Land, LandMedia
from app.object.schemas.land import LandCreate, LandUpdate, LandResponse
from app.utils.file_utils import save_upload_file

from app.object.functions.validations.validate_land import validate_land


def generate_crm_id(mapper, connection, target):
    session = Session(bind=connection)
    max_id = session.query(Land.id).order_by(Land.id.desc()).first()
    next_id = (max_id[0] + 1) if max_id else 1
    target.crm_id = f"A{next_id}"


event.listen(Land, 'before_insert', generate_crm_id)


async def create_land(db: AsyncSession, land: LandCreate, media: [UploadFile]):
    try:
        print(land.phone_number[1:])
        land_validation = await validate_land(db, land)

        if land_validation:
            land.responsible = 'agent'
            db_land = Land(**land.model_dump())
            db.add(db_land)
            await db.commit()
            await db.refresh(db_land)

            urls = save_upload_file(media, db_land.id)
            for ulr in urls:
                db_land_image = LandMedia(land_id=db_land.id, url=ulr)
                db.add(db_land_image)
                await db.commit()
                await db.refresh(db_land_image)

                db_land.media.append(db_land_image)

            await db.commit()
            await db.refresh(db_land)

            print(db_land)
            land_response = LandResponse.model_validate(db_land)
            return jsonable_encoder(land_response)
    except IntegrityError as e:
        if 'duplicate key value violates unique constraint' in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Land already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def get_land(db: AsyncSession, land_id: int):
    result = await db.execute(select(Land).filter_by(id=land_id))
    land = result.scalars().first()
    if not land:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Land not found")

    return land
