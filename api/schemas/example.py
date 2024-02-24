from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str

    class Config:
        from_attributes = True


class UserRead(UserBase):
    id: int


class UserCreate(UserBase):
    pass
