from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Annotated

from app.object.models import ActionType
from app.report.Accounting.funcs import get_overall_data
from app.report.deals.model import Deal
from app.database import get_async_session
from app.auth.utils import get_current_user
from app.auth.schema import UserRead

router = APIRouter()


@router.get("/overall_data")
async def get_overall_data_api(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[UserRead, Depends(get_current_user)],
    action_type: ActionType,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    date: Optional[str] = None,
    responsible: Optional[str] = None,
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    
    return await get_overall_data(db, action_type, start_date, end_date, date, responsible)