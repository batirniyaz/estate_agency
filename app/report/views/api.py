from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schema import UserRead
from app.auth.utils import get_current_active_user
from app.database import get_async_session
from app.object.models import ActionType

from app.report.views.crud import create_view, get_views, get_view, update_view, delete_view
from app.report.views.schema import ViewCreate, ViewResponse, ViewUpdate

router = APIRouter()


@router.post("/", response_model=ViewResponse)
async def create_view_endpoint(
    view: ViewCreate,
    background_tasks: BackgroundTasks,
    current_user: Annotated[UserRead, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_async_session),
):
    return await create_view(db, view, background_tasks)


@router.get("/")
async def get_views_endpoint(
    current_user: Annotated[UserRead, Depends(get_current_active_user)],
    action_type: ActionType,
    limit: int = 10,
    page: int = 1,
    db: AsyncSession = Depends(get_async_session),
):
    return await get_views(db, action_type, limit, page)


@router.get("/{view_id}", response_model=ViewResponse)
async def get_view_endpoint(
    view_id: int,
    current_user: Annotated[UserRead, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_async_session),
):
    return await get_view(db, view_id)


@router.put("/{view_id}", response_model=ViewResponse)
async def update_view_endpoint(
    view_id: int,
    view: ViewUpdate,
    background_tasks: BackgroundTasks,
    current_user: Annotated[UserRead, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_async_session),
):
    return await update_view(db, view_id, view, current_user, background_tasks)


@router.delete("/{view_id}")
async def delete_view_endpoint(
    view_id: int,
    current_user: Annotated[UserRead, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_async_session),
):
    return await delete_view(db, view_id)

