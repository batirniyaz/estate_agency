from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth.utils import get_users
from app.object.models.apartment import Apartment
from app.object.models.commercial import Commercial
from app.object.models.land import Land
from app.report.clients.schema import ClientCreate

async def validate_client(db: AsyncSession, client: ClientCreate):
    if client.responsible:
        agents = await get_users(db)
        if client.responsible not in [agent.full_name for agent in agents]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Responsible agent not found")

    if client.hot_clients:
        if client.hot_clients < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The number of hot clients can not be negative')

    if client.cold_clients:
        if client.cold_clients < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The number of cold clients can not be negative')

    if client.calls:
        if client.calls < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The number of calls can not be negative')
