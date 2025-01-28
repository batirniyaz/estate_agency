
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Annotated

from app.object.models import ActionType
from app.report.Accounting.funcs import get_overall_data
from app.database import get_async_session
from app.auth.utils import get_current_user
from app.auth.schema import UserRead

router = APIRouter()


@router.get("/overall_data")
async def get_overall_data_api(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[UserRead, Depends(get_current_user)],
    action_type: ActionType,
    start_date: Optional[str] = Query(None, description="Дата начала в формате YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="Дата окончания в формате YYYY-MM-DD"),
    date: Optional[str] = Query(None, description="Дата в формате YYYY-MM-DD или YYYY-MM или YYYY или YYYY-W52"),
    responsible: Optional[str] = None,
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    
    return await get_overall_data(db=db, action_type=action_type if action_type else None,
                                  start_date=start_date if start_date else None,
                                  end_date=end_date if end_date else None, date=date if date else None,
                                  responsible=responsible if responsible else None,
                                  current_user=current_user)