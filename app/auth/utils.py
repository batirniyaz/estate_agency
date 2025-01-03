from datetime import timedelta, datetime
from typing import Annotated, Set
import pytz
from sqlalchemy import func

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from fastapi import Form, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.model import User, LoginInfo
from app.auth.schema import TokenData, UserRead, UserCreate, UserResponse, UserUpdate
from app.config import SECRET, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.database import get_async_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

token_blacklist: Set[str] = set()


class CustomOAuth2PasswordRequestForm:
    def __init__(
        self,
        phone: Annotated[str, Form()],
        password: Annotated[str, Form()],
    ):
        self.phone = phone
        self.password = password


def blacklist_token(token: str):
    token_blacklist.add(token)


def is_token_blacklisted(token: str) -> bool:
    return token in token_blacklist


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


async def get_user(db: AsyncSession, phone: str):
    res = await db.execute(select(User).filter_by(phone=phone))
    user = res.scalars().first()
    return user


async def authenticate_user(db: AsyncSession, phone: str, password: str):
    user = await get_user(db, phone)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    current_tz = pytz.timezone('Asia/Tashkent')
    if expires_delta:
        expire = datetime.now(current_tz) + expires_delta
    else:
        expire = datetime.now(current_tz) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if is_token_blacklisted(token):
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        phone: str = payload.get("sub")
        if phone is None:
            raise credentials_exception
        token_data = TokenData(phone=phone)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(db, phone=token_data.phone)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserRead, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Неактивный пользователь")
    return current_user


async def create_user(db: AsyncSession, user: UserCreate):
    if len(user.phone) > 13 or len(user.phone) < 13:
        raise HTTPException(status_code=400, detail="Номер телефона слишком длинный или слишком короткий")

    try:
        print(user)
        hashed_password = get_password_hash(user.hashed_password)

        user = User(
            hashed_password=hashed_password,
            phone=user.phone,
            email=user.email,
            full_name=user.full_name,
            is_superuser=False if user.is_superuser else False
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return UserResponse(**user.__dict__)
    except IntegrityError as e:
        await db.rollback()
        if "unique constraint" in str(e.orig):
            raise HTTPException(status_code=400, detail="Телефон или адрес электронной почты пользователя уже существует")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_users(db: AsyncSession):
    res = await db.execute(select(User))
    users = res.scalars().all()
    return users or []


async def get_user_by_id(db: AsyncSession, user_id: int):
    res = await db.execute(select(User).filter_by(id=user_id))
    user = res.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь с идентификатором не найден")

    return user


async def get_user_by_email(db: AsyncSession, user_email: str):
    res = await db.execute(select(User).filter_by(email=user_email))
    user = res.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь с адресом электронной почты не найден")

    return user


async def get_user_by_name(db: AsyncSession, name: str):
    res = await db.execute(select(User).filter_by(full_name=name))
    user = res.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь с именем не найден")

    return user


async def update_user(db: AsyncSession, user_id: int, user: UserUpdate):
    res_phone = await db.execute(select(User).filter_by(phone=user.phone))
    user_phone = res_phone.scalars().first()
    if user_phone:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Пользователь с таким телефоном уже существует')

    res_email = await db.execute(select(User).filter_by(email=user.email))
    user_email = res_email.scalars().first()
    if user_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Пользователь с таким адресом электронной почты уже существует')

    user_db = await get_user_by_id(db, user_id)

    try:
        if user.hashed_password:
            hashed_pass = get_password_hash(user.hashed_password)
            user.hashed_password = hashed_pass

        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(user_db, key, value)

        await db.commit()
        return user_db
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user_by_id(db, user_id)
    try:
        await db.delete(user)
        await db.commit()
        return {"detail": "Пользователь успешно удален"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def read_me(current_user, token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    current_tz = pytz.timezone('Asia/Tashkent')
    new_expire = datetime.now(current_tz) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    payload['exp'] = new_expire
    new_token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)

    return {"user": current_user, "token": new_token}


async def log_login_info(db: AsyncSession, user_id, email, phone):
    try:
        login_info = LoginInfo(user_id=user_id, email=email, phone=phone)
        db.add(login_info)
        await db.commit()
        await db.refresh(login_info)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_login_info(db: AsyncSession, limit: int = 10, page: int = 1):
    try:
        res = await db.execute(select(LoginInfo).limit(limit).offset((page - 1) * limit).order_by(LoginInfo.id.desc()))
        login_info = res.scalars().all()

        total_count = await db.scalar(select(func.count(LoginInfo.id)))
        return {"data": login_info or [], "total_count": total_count}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
