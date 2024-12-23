from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.report.validations.view_validate import validate_view
from app.report.views.model import View
from app.report.views.schema import ViewCreate, ViewUpdate, ViewResponse


async def create_view(db: AsyncSession, view: ViewCreate):

    await validate_view(db, view)

    try:
        db_view = View(**view.model_dump())
        db.add(db_view)
        await db.commit()
        await db.refresh(db_view)
        return db_view
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_views(db: AsyncSession, limit: int = 10, page: int = 1):
    res = await db.execute(select(View).limit(limit).offset((page - 1) * limit))
    views = res.scalars().all()
    total_count = await db.scalar(select(func.count(View.id)))

    return {"data": views or [], "total_count": total_count}


async def get_view(db: AsyncSession, view_id: int):
    res = await db.execute(select(View).filter_by(id=view_id))
    view = res.scalars().first()

    if not view:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="View not found")

    return view


async def update_view(db: AsyncSession, view_id: int, view: ViewUpdate):
    await validate_view(db, view)

    try:
        db_view = await get_view(db, view_id)

        for key, value in view.model_dump(exclude_unset=True).items():
            setattr(db_view, key, value)

        await db.commit()
        await db.refresh(db_view)
        return db_view
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete_view(db: AsyncSession, view_id: int):
    try:
        db_view = await get_view(db, view_id)
        await db.delete(db_view)
        await db.commit()
        return {"message": "View deleted successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))