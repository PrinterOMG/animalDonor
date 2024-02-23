from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str | None
    second_name: str | None
    email: str
    is_active: bool


class UserRead(UserBase):
    id: int
