from datetime import timedelta, timezone, datetime
from typing import Annotated, Set

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from fastapi import Form, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.model import User
from app.auth.schema import TokenData, UserRead, UserCreate, UserResponse
from app.config import SECRET, ALGORITHM
from app.database import get_async_session, async_session_maker

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

token_blacklist: Set[str] = set()


def blacklist_token(token: str):
    token_blacklist.add(token)


def is_token_blacklisted(token: str) -> bool:
    return token in token_blacklist


class CustomOAuth2PasswordRequestForm:
    def __init__(
        self,
        phone: Annotated[str, Form()],
        password: Annotated[str, Form()],
    ):
        self.phone = phone
        self.password = password


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
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
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
    db: AsyncSession = await get_async_session().__anext__()
    user = await get_user(db, phone=token_data.phone)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserRead, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def create_user(db: AsyncSession, user: UserCreate):
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
        if "unique constraint" in str(e.orig):
            raise HTTPException(status_code=400, detail="User phone or email already exists")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def create_superuser():

    async with async_session_maker() as session:
        async with session.begin():
            result = await session.execute(select(User).filter_by(is_superuser=True))
            superuser = result.scalars().first()

            if not superuser:
                superuser = User(
                    phone="+998999999999",
                    email="admin@example.com",
                    full_name="Super User",
                    hashed_password=get_password_hash("admin"),
                    is_superuser=True,
                    disabled=False
                )
                session.add(superuser)
                await session.commit()


