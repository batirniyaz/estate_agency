from fastapi import HTTPException, status, BackgroundTasks
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.object.models import ActionType
from app.object.models.apartment import Apartment
from app.report.deals.crud import create_deal
from app.report.validations.view_validate import validate_view
from app.report.views.model import View
from app.report.views.schema import ViewCreate, ViewUpdate


async def create_view(db: AsyncSession, view: ViewCreate, bg_tasks: BackgroundTasks = None):

    await validate_view(db, view)

    if view.crm_id[0] == 'A':
        res = await db.execute(select(Apartment).filter_by(id=int(view.crm_id[1:])))
        obj = res.scalars().first()
        if obj:
            view.owner_number = obj.phone_number

    try:
        view.commission = view.agent_percent * view.price / 100

        db_view = View(**view.model_dump())
        db.add(db_view)
        await db.commit()
        await db.refresh(db_view)

        if db_view.status_deal:
            bg_tasks.add_task(create_deal, db=db, action_type=db_view.action_type, responsible=db_view.responsible,
                              date=db_view.date, crm_id=db_view.crm_id, object_price=db_view.price,
                              commission=db_view.commission, agent_percent=db_view.agent_percent)

        return db_view
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_views(db: AsyncSession, action_type: ActionType, limit: int = 10, page: int = 1):
    res = await db.execute(select(View).filter_by(action_type=action_type).limit(limit).offset((page - 1) * limit).order_by(View.id.desc()))
    views = res.scalars().all()
    total_count = await db.scalar(select(func.count(View.id)).filter_by(action_type=action_type))

    return {"data": views or [], "total_count": total_count}


async def get_view(db: AsyncSession, view_id: int):
    res = await db.execute(select(View).filter_by(id=view_id))
    view = res.scalars().first()

    if not view:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Показ не найден")

    return view


async def update_view(db: AsyncSession, view_id: int, view: ViewUpdate, current_user, bg_tasks: BackgroundTasks = None):

    db_view = await get_view(db, view_id)
    if not current_user.is_superuser and db_view.responsible != current_user.full_name:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы не можете редактировать этот показ")

    if db_view.status_deal:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Нельзя редактировать завершенный показ")

    await validate_view(db, view)

    if view.crm_id[0] == 'A':
        res = await db.execute(select(Apartment).filter_by(id=int(view.crm_id[1:])))
        obj = res.scalars().first()
        if obj:
            view.owner_number = obj.phone_number

    try:

        for key, value in view.model_dump(exclude_unset=True).items():
            setattr(db_view, key, value)

        db_view.commission = db_view.agent_percent * db_view.price / 100

        await db.commit()
        await db.refresh(db_view)

        if db_view.status_deal:
            bg_tasks.add_task(create_deal, db=db, action_type=db_view.action_type, responsible=db_view.responsible,
                              date=db_view.date, crm_id=db_view.crm_id, object_price=db_view.price,
                              commission=db_view.commission, agent_percent=db_view.agent_percent)

        return db_view
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete_view(db: AsyncSession, view_id: int):
    db_view = await get_view(db, view_id)
    try:
        await db.delete(db_view)
        await db.commit()
        return {"message": "Показ удален"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))