from pydantic import BaseModel


class PetTypeBase(BaseModel):
    name: str


class PetTypeRead(PetTypeBase):
    id: int
