from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import get_users
from app.report.clients.schema import ClientCreate

async def validate_client(db: AsyncSession, client: ClientCreate):
    if client.responsible:
        agents = await get_users(db)
        if client.responsible not in [agent.full_name for agent in agents]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ответственный агент не найден")

    if client.hot_clients:
        if client.hot_clients < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Количество горячих клиентов не может быть отрицательным')

    if client.cold_clients:
        if client.cold_clients < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Количество холодных клиентов не может быть отрицательным')

    if client.calls:
        if client.calls < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Количество звонков не может быть отрицательным')
