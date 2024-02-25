from pydantic import BaseModel


class PetTypeBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class PetTypeRead(PetTypeBase):
    id: int
