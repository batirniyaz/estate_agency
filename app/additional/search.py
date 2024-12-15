from operator import attrgetter
import logging

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.object.models.apartment import Apartment
from app.object.models.commercial import Commercial
from app.object.models.land import Land

logger = logging.getLogger(__name__)


async def search(db: AsyncSession, text: str):
    matched_objects = []
    try:
        land_res = select(Land).where(Land.title.ilike(f'%{text}%'))
        db_land = await db.execute(land_res)
        matched_objects.extend(db_land.scalars().all())

        apartment_res = select(Apartment).where(Apartment.title.ilike(f'%{text}%'))
        db_apartment = await db.execute(apartment_res)
        matched_objects.extend(db_apartment.scalars().all())

        commercial_res = select(Commercial).where(Commercial.title.ilike(f'%{text}%'))
        db_commercial = await db.execute(commercial_res)
        matched_objects.extend(db_commercial.scalars().all())

        matched_objects = sorted(matched_objects, key=attrgetter('id'))
        return matched_objects
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_all_object(db: AsyncSession):
    land_count = await db.scalar(select(func.count(Land.id)))
    apartment_count = await db.scalar(select(func.count(Apartment.id)))
    commercial_count = await db.scalar(select(func.count(Commercial.id)))

    return {
        "land": land_count,
        "apartment": apartment_count,
        "commercial": commercial_count,
        "total": land_count + apartment_count + commercial_count
    }
