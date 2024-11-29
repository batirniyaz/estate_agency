from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.metro.model import Metro
from app.metro.schema import MetroCreate, MetroUpdate


async def create_metro(db: AsyncSession, metro: MetroCreate):
    try:
        db_metro = Metro(**metro.model_dump())
        db.add(db_metro)
        await db.commit()
        await db.refresh(db_metro)

        return db_metro
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_metros(db: AsyncSession):
    result = await db.execute(select(Metro))
    metros = result.scalars().all()
    return metros if metros else []


async def get_metro(db: AsyncSession, metro_id: int):
    db_metro = await db.execute(select(Metro).filter_by(id=metro_id))
    db_metro = db_metro.scalar_one_or_none()

    if not db_metro:
        raise HTTPException(status_code=404, detail="Metro not found")

    return db_metro


async def update_metro(db: AsyncSession, metro_id: int, metro: MetroUpdate):
    try:
        db_metro = await get_metro(db, metro_id)

        for key, value in metro.model_dump(exclude_unset=True).items():
            setattr(db_metro, key, value)

        await db.commit()

        return db_metro
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_metro(db: AsyncSession, metro_id: int):
    db_metro = await get_metro(db, metro_id)
    await db.delete(db_metro)
    await db.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Metro deleted successfully")
