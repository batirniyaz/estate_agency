from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.changes.funcs import get_changes_log
from app.database import get_async_session
from app.auth.schema import UserRead
from app.auth.utils import get_current_active_user

router = APIRouter()


@router.get("/")
async def get_changes_log_endpoint(
        current_user: UserRead = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_async_session),
        limit: int = 10,
        page: int = 1,
):
    return await get_changes_log(db, limit, page)
