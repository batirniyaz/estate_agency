
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth.utils import get_users
from app.object.models.apartment import Apartment
from app.object.models.commercial import Commercial
from app.object.models.land import Land
from app.report.views.schema import ViewCreate


async def validate_view(db: AsyncSession, view: ViewCreate):
    if view.responsible:
        agents = await get_users(db)
        if view.responsible not in [agent.full_name for agent in agents]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ответственный агент не найден")

    if view.object_sum or view.commission_sum:
        if view.object_sum < 0 or view.commission_sum < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Сумма комиссии и стоимость объекта не могут быть отрицательными")

    if view.agent_percent:
        if view.agent_percent > 100 or view.agent_percent < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Процент агента должен быть в пределах от 0 до 100")

    if view.crm_id:
        if len(view.crm_id) < 2 or view.crm_id[0] not in ['A', 'C', 'L']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный формат crm id")

        table_mapping = {
            'A': Apartment,
            'C': Commercial,
            'L': Land
        }
        table_obj = table_mapping.get(view.crm_id[0])
        res = await db.execute(select(table_obj).filter_by(id=int(view.crm_id[1:])))
        obj = res.scalars().first()
        if not obj:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Объект не найден")

