from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, Field

from api.schemas.pet_type import PetTypeRead


class PetBase(BaseModel):
    name: str
    breed: str
    blood_type: str
    birthday: date
    weight: float
    role: str

    class Config:
        from_attributes = True


class PetRead(PetBase):
    id: int

    pet_type: PetTypeRead


class PetUpdate(PetBase):
    pass


class PetCreate(PetBase):
    name: Annotated[str, Field(min_length=2)]
    weight: Annotated[float, Field(gt=0)]
    pet_type_id: Annotated[int, Field(ge=0, le=4)]
    role: Literal['donor', 'recipient']
    owner_id: int

