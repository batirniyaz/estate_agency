from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.district.model import District
from app.district.schema import DistrictCreate, DistrictUpdate


async def create_district(db: AsyncSession, district: DistrictCreate):
    try:
        db_district = District(**district.model_dump())
        db.add(db_district)
        await db.commit()
        await db.refresh(db_district)

        return db_district
    except IntegrityError as e:
        await db.rollback()
        if "duplicate key value violates unique constraint" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="District already exists")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_districts(db: AsyncSession):
    result = await db.execute(select(District))
    districts = result.scalars().all()
    return districts if districts else []


async def get_district(db: AsyncSession, district_id: int):
    db_district = await db.execute(select(District).filter_by(id=district_id))
    db_district = db_district.scalar_one_or_none()

    if not db_district:
        raise HTTPException(status_code=404, detail="District not found")

    return db_district


async def update_district(db: AsyncSession, district_id: int, district: DistrictUpdate):
    db_district = await get_district(db, district_id)
    db_districts = await get_districts(db)
    if district.name in [d.name for d in db_districts]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="District already exists")

    try:

        for key, value in district.model_dump(exclude_unset=True).items():
            setattr(db_district, key, value)

        await db.commit()

        return db_district
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def delete_district(db: AsyncSession, district_id: int):
    db_district = await get_district(db, district_id)
    await db.delete(db_district)
    await db.commit()
    return HTTPException(status_code=status.HTTP_200_OK, detail="District deleted")
