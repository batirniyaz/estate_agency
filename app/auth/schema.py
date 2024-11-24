from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import datetime


class Token(BaseModel):
    access_token: str = Field(..., description="The access token")
    token_type: str = Field(..., description="The token type")


class TokenData(BaseModel):
    phone: Optional[str] = Field(None, description="The phone number of the user")


class UserCreate(BaseModel):
    phone: str = Field(..., description="The phone number of the user")
    email: EmailStr = Field(..., description="The email of the user")
    full_name: str = Field(..., description="The full name of the user")
    hashed_password: str = Field(..., description="The hashed password of the user")
    is_superuser: bool = Field(False, description="The role of the user")


class UserUpdate(UserCreate):
    phone: Optional[str] = Field(None, description="The phone number of the user")
    email: Optional[str] = Field(None, description="The email of the user")
    full_name: Optional[str] = Field(None, description="The full name of the user")
    hashed_password: Optional[str] = Field(None, description="The hashed password of the user")


class UserRead(UserCreate):
    id: int = Field(..., description="The ID of the user")
    disabled: bool = Field(..., description="The status of the user")
    is_superuser: bool = Field(..., description="The role of the user")
    created_at: datetime.datetime = Field(..., description="The time the user was created")
    updated_at: datetime.datetime = Field(..., description="The time the user was updated")


class UserResponse(BaseModel):
    id: int = Field(..., description="The ID of the user")
    phone: str = Field(..., description="The phone number of the user")
    email: str = Field(..., description="The email of the user")
    full_name: str = Field(..., description="The full name of the user")
    is_superuser: bool = Field(..., description="The role of the user")


class UserInDB(UserRead):
    hashed_password: str = Field(..., description="The hashed password of the user")
