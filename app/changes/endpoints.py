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
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Только администратор может просматривать журнал изменений')
    return await get_changes_log(db, limit, page)
