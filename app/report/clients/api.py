from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schema import UserRead
from app.auth.utils import get_current_active_user
from app.report.clients.crud import create_client, get_clients, get_client, update_client, delete_client
from app.report.clients.schema import ClientCreate, ClientResponse, ClientUpdate
from app.database import get_async_session

router = APIRouter()

@router.post("/", response_model=ClientResponse)
async def create_client_endpoint(
    client: ClientCreate,
    current_user: Annotated[UserRead, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_async_session),
):
    return await create_client(db, client)


@router.get("/")
async def get_clients_endpoint(
    current_user: Annotated[UserRead, Depends(get_current_active_user)],
    limit: int = 10,
    page: int = 1,
    db: AsyncSession = Depends(get_async_session),
):
    return await get_clients(db, limit, page)


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client_endpoint(
    client_id: int,
    current_user: Annotated[UserRead, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_async_session),
):
    return await get_client(db, client_id)


@router.put("/{client_id}", response_model=ClientResponse)
async def update_client_endpoint(
    client_id: int,
    client: ClientUpdate,
    current_user: Annotated[UserRead, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_async_session),
):
    return await update_client(db, client_id, client)


@router.delete("/{client_id}")
async def delete_client_endpoint(
    client_id: int,
    current_user: Annotated[UserRead, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_async_session),
):
    return await delete_client(db, client_id)
