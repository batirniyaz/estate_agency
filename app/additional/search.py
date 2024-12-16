from operator import attrgetter
import logging

from fastapi import HTTPException, status
from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.object.models.apartment import Apartment
from app.object.models.commercial import Commercial
from app.object.models.land import Land

logger = logging.getLogger(__name__)


async def search(db: AsyncSession, text: str, table: str):
    table_mapping = {
        "land": Land,
        "apartment": Apartment,
        "commercial": Commercial
    }
    table_obj = table_mapping.get(table)
    if not table_obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid table name")

    matched_objects = []
    try:
        res = select(table_obj).where(or_(
            table_obj.title.ilike(f'%{text}%'),
            table_obj.crm_id.ilike(f'%{text}%'),
            )
        )
        db_res = await db.execute(res)
        matched_objects.extend(db_res.scalars().all())

    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return matched_objects


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
