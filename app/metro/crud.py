from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
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
    except IntegrityError as e:
        await db.rollback()
        if "duplicate key value violates unique constraint" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Метро с таким именем уже существует")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_metros(db: AsyncSession):
    result = await db.execute(select(Metro))
    metros = result.scalars().all()
    return metros if metros else []


async def get_metro(db: AsyncSession, metro_id: int):
    db_metro = await db.execute(select(Metro).filter_by(id=metro_id))
    db_metro = db_metro.scalar_one_or_none()

    if not db_metro:
        raise HTTPException(status_code=404, detail="Метро не найдено")

    return db_metro


async def update_metro(db: AsyncSession, metro_id: int, metro: MetroUpdate):

    db_metro = await get_metro(db, metro_id)
    db_metros = await get_metros(db)
    if metro.name in [d.name for d in db_metros]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Метро с таким именем уже существует")

    try:

        for key, value in metro.model_dump(exclude_unset=True).items():
            setattr(db_metro, key, value)

        await db.commit()

        return db_metro
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def delete_metro(db: AsyncSession, metro_id: int):
    db_metro = await get_metro(db, metro_id)
    await db.delete(db_metro)
    await db.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Метро успешно удалено")
