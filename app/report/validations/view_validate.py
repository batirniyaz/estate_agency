
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth.utils import get_users
from app.district.crud import get_districts
from app.object.models.apartment import Apartment
from app.object.models.commercial import Commercial
from app.object.models.land import Land
from app.report.views.schema import ViewCreate


async def validate_view(db: AsyncSession, view: ViewCreate):
    if view.responsible:
        agents = await get_users(db)
        if view.responsible not in [agent.full_name for agent in agents]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ответственный агент не найден")

    if view.district:
        districts = await get_districts(db)
        if view.district not in [district.name for district in districts]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Район не найден")

    if view.price:
        if view.price < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Цена не может быть отрицательной")

    if view.commission:
        if view.commission < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Комиссия не может быть отрицательной")

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

