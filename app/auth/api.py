from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schema import Token, UserRead, UserCreate, UserUpdate
from app.auth.utils import CustomOAuth2PasswordRequestForm, authenticate_user, create_access_token, \
    get_current_active_user, create_user, blacklist_token, log_login_info, get_login_info, get_users, get_user_by_id, \
    update_user, delete_user, read_me, get_user_by_email
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.database import get_async_session
from user_agents import parse

from .forgot_pass import forgot_password
from .utils import oauth2_scheme

router = APIRouter()


@router.post("/login")
async def login(
        request: Request,
        form_data: Annotated[CustomOAuth2PasswordRequestForm, Depends()],
        db: Annotated[AsyncSession, Depends(get_async_session)],
) -> Token:
    print(parse(request.headers.get("user-agent")))
    user = await authenticate_user(db, form_data.phone, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный номер телефона или пароль",
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
    return {"msg": "Успешно вышли из системы"}


router_user = APIRouter()


@router_user.post("/")
async def register_user(
        user: UserCreate,
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="У вас нет прав на создание пользователей")
    return await create_user(db, user)


@router_user.get("/")
async def get_users_endpoint(
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
):
    return await get_users(db)


@router_user.get('/{user_id}')
async def get_user_by_id_endpoint(
        user_id: int,
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="У вас нет прав на просмотр пользователей")
    return await get_user_by_id(db, user_id)


@router_user.put('/{user_id}')
async def update_user_endpoint(
        user_id: int,
        user: UserUpdate,
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="У вас нет прав на обновление пользователей")
    return await update_user(db, user_id, user)


@router_user.delete('/{user_id}')
async def delete_user_endpoint(
        user_id: int,
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="У вас нет прав на удаление пользователей")
    return await delete_user(db, user_id)


@router.get("/me/", response_model={})
async def read_user_me(
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        token: Annotated[str, Depends(oauth2_scheme)]
):
    return await read_me(current_user, token)


@router.get("/login_info/")
async def get_login_info_endpoint(
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
        limit: int = 10,
        page: int = 1
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="У вас нет прав на просмотр логов входа")
    return await get_login_info(db, limit, page)


@router.post("/forgot_password/")
async def forgot_password_endpoint(
        email: str,
        db: Annotated[AsyncSession, Depends(get_async_session)],
        code: str = None,
        new_password: str = None
):
    user = await get_user_by_email(db, email)
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="У вас нет прав на сброс пароля")

    return await forgot_password(db=db, email=email, code=code if code else None,
                                 new_password=new_password if new_password else None)
