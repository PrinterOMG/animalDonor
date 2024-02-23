from typing import Annotated

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    first_name: str | None
    second_name: str | None


class UserRead(UserBase):
    id: int
    email: str
    is_active: bool


class UserUpdate(UserBase):
    first_name: Annotated[str | None, Field(min_length=2)] = None
    second_name: Annotated[str | None, Field(min_length=2)] = None
