from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def generate_crm_id(db: AsyncSession, my_object, letter):
    res = await db.execute(select(my_object).order_by(my_object.id.desc()).limit(1))
    max_id = res.scalar()
    next_id = (max_id.id + 1) if max_id else 1
    crm_id = f"{letter}{next_id}"
    return crm_id
