from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import get_users
from app.district.crud import get_districts
from app.report.clients.schema import ClientCreate

async def validate_client(db: AsyncSession, client: ClientCreate):
    if client.responsible:
        agents = await get_users(db)
        if client.responsible not in [agent.full_name for agent in agents]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ответственный агент не найден")

    if client.district:
        districts = await get_districts(db)
        for district in client.district:
            if district not in [district.name for district in districts]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Район не найден")

    if client.budget:
        if client.budget < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Бюджет не может быть отрицательным")
