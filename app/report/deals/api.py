from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schema import UserRead
from app.auth.utils import get_current_active_user
from app.object.models import ActionType
from app.report.deals.crud import get_deals, get_deal, delete_deal
from app.database import get_async_session

router = APIRouter()


@router.get("/")
async def get_deals_endpoint(
    current_user: Annotated[UserRead, Depends(get_current_active_user)],
    action_type: ActionType,
    limit: int = 10,
    page: int = 1,
    db: AsyncSession = Depends(get_async_session),
):
    return await get_deals(db, action_type, limit, page)


@router.get("/{deal_id}")
async def get_deal_endpoint(
    deal_id: int,
    current_user: Annotated[UserRead, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_async_session),
):
    return await get_deal(db, deal_id)


@router.delete("/{deal_id}")
async def delete_deal_endpoint(
    deal_id: int,
    current_user: Annotated[UserRead, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_async_session),
):
    return await delete_deal(db, deal_id)