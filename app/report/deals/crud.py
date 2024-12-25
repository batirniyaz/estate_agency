from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.object.models import ActionType
from app.report.deals.model import Deal


async def create_deal(db: AsyncSession,
                     action_type: ActionType,
                     responsible: str,
                     date: str,
                     crm_id: str,
                     object_price: int,
                     commission: float,
                     agent_percent: int):
    try:
        db_deal = Deal(action_type=action_type,
                       responsible=responsible,
                       date=date,
                       crm_id=crm_id,
                       object_price=object_price,
                       commission=commission,
                       agent_percent=agent_percent)
        db.add(db_deal)
        await db.commit()
        await db.refresh(db_deal)
        return db_deal
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_deals(db: AsyncSession, limit: int = 10, page: int = 1):
    res = await db.execute(select(Deal).limit(limit).offset((page - 1) * limit))
    deals = res.scalars().all()
    total_count = await db.scalar(select(func.count(Deal.id)))

    return {"data": deals or [], "total_count": total_count}


async def get_deal(db: AsyncSession, deal_id: int):
    res = await db.execute(select(Deal).filter_by(id=deal_id))
    deal = res.scalars().first()

    if not deal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сделка не найдена")

    return deal


async def delete_deal(db: AsyncSession, deal_id: int):
    deal = await get_deal(db, deal_id)
    await db.delete(deal)
    await db.commit()
    return {"message": "Сделка удалена"}
