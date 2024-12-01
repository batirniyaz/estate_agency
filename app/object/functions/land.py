from fastapi import HTTPException, status, UploadFile
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.object.models.land import Land
from app.object.schemas.land import LandCreate, LandUpdate


def generate_crm_id(mapper, connection, target):
    session = Session(bind=connection)
    max_id = session.query(Land.id).order_by(Land.id.desc()).first()
    next_id = (max_id[0] + 1) if max_id else 1
    target.crm_id = f"A{next_id}"


event.listen(Land, 'before_insert', generate_crm_id)


async def create_land(db: AsyncSession, land: LandCreate, media: [UploadFile]):
    try:
        land = Land(**land.model_dump())
        db.add(land)
        await db.commit()
        await db.refresh(land)
        return land
    except IntegrityError as e:
        if 'duplicate key value violates unique constraint' in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Land already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def get_land(db: AsyncSession, land_id: int):
    result = await db.execute(select(Land).filter_by(id=land_id))
    lands = result.scalars().first()
    return lands if lands else None
