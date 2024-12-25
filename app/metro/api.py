from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schema import UserRead
from app.auth.utils import get_current_active_user
from app.database import get_async_session
from app.metro.crud import create_metro, get_metros, get_metro, update_metro, delete_metro
from app.metro.schema import MetroResponse, MetroCreate, MetroUpdate

router = APIRouter()


@router.post("/", response_model=MetroResponse)
async def create_metro_endpoint(
        metro: MetroCreate,
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_async_session),
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="У вас нет прав на создание метро")
    return await create_metro(db, metro)


@router.get("/", response_model=list[MetroResponse])
async def get_metros_endpoint(
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_async_session)
):
    return await get_metros(db)


@router.get("/{metro_id}", response_model=MetroResponse)
async def get_metro_endpoint(
        metro_id: int,
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_async_session)
):
    return await get_metro(db, metro_id)


@router.put("/{metro_id}", response_model=MetroResponse)
async def update_metro_endpoint(
        metro_id: int,
        metro: MetroUpdate,
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_async_session)
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="У вас нет прав на обновление метро")
    return await update_metro(db, metro_id, metro)


@router.delete("/{metro_id}")
async def delete_metro_endpoint(
        metro_id: int,
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_async_session)
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="У вас нет прав на удаление метро")
    return await delete_metro(db, metro_id)
