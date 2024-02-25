from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    first_name: str | None
    second_name: str | None
    patronymic: str | None

    phone: str | None
    city: str | None
    is_email_public: bool

    class Config:
        from_attributes = True


class UserRead(UserBase):
    id: int
    email: str
    is_active: bool
    avatar: str | None
    created_at: datetime
    is_email_confirm: bool


class UserUpdate(UserBase):
    first_name: Annotated[str | None, Field(min_length=2)] = None
    second_name: Annotated[str | None, Field(min_length=2)] = None
    patronymic: Annotated[str | None, Field(min_length=2)] = None

    phone: Annotated[str | None, Field(pattern=r'^\+7\d{10}$')] = None
    city: Annotated[str | None, Field()] = None
    is_email_public: Annotated[bool | None, Field()] = None
