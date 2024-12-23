from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, TIMESTAMP, Boolean

import datetime

from app.database import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    phone: Mapped[str] = mapped_column(String(length=13), unique=True)
    email: Mapped[str] = mapped_column(String(length=255), unique=True)
    full_name: Mapped[str] = mapped_column(String(length=255))
    hashed_password: Mapped[str] = mapped_column(String(length=255))
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))


class LoginInfo(Base):
    __tablename__ = 'login_info'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer)
    email: Mapped[str] = mapped_column(String(length=255))
    phone: Mapped[str] = mapped_column(String(length=13))
    login_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                        default=lambda: datetime.datetime.now(datetime.timezone.utc))


class PasswordReset(Base):
    __tablename__ = 'password_reset'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    reset_code: Mapped[str] = mapped_column(String(length=6))
    email: Mapped[str] = mapped_column(String(length=255))
