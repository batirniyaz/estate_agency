from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schema import Token, UserRead, UserCreate
from app.auth.utils import CustomOAuth2PasswordRequestForm, authenticate_user, create_access_token, \
    get_current_active_user, create_user, blacklist_token, log_login_info, get_login_info
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.database import get_async_session
from user_agents import parse

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/login")
async def login(
        request: Request,
        form_data: Annotated[CustomOAuth2PasswordRequestForm, Depends()],
        db: AsyncSession = Depends(get_async_session),
) -> Token:
    print(parse(request.headers.get("user-agent")))
    user = await authenticate_user(db, form_data.phone, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone number or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    await log_login_info(db, user.id, user.email, user.phone)
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.phone}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/logout")
async def logout(
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        token: Annotated[str, Depends(oauth2_scheme)],
):
    blacklist_token(token)
    return {"msg": "Successfully logged out"}


@router.post("/create")
async def register_user(
        user: UserCreate,
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_async_session),
):
    try:
        if not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to create users")
        return await create_user(db, user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/me/", response_model=UserRead)
async def read_users_me(
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
):
    return current_user


@router.get("/me/items/")
async def read_own_items(
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@router.get("/login_info/")
async def get_login_info_endpoint(db: AsyncSession = Depends(get_async_session)):
    return await get_login_info(db)
