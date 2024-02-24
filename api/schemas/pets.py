from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, Field

from api.schemas.pet_type import PetTypeRead
from api.schemas.unavaible_list import UnavailableListRead
from api.schemas.vaccination import VaccinationRead


class PetBase(BaseModel):
    name: str
    breed: str
    blood_type: str
    birthday: date
    weight: float

    class Config:
        from_attributes = True


class PetRead(PetBase):
    id: int

    role: str
    pet_type: PetTypeRead
    unavailable_lists: list[UnavailableListRead]
    vaccinations: list[VaccinationRead]


class PetUpdate(PetBase):
    name: str | None = None
    breed: str | None = None
    blood_type: str | None = None
    birthday: date | None = None
    weight: float | None = None
    pet_type_id: int | None = None


class PetCreate(PetBase):
    name: Annotated[str, Field(min_length=2)]
    weight: Annotated[float, Field(gt=0)]
    pet_type_id: int
    role: Literal['donor', 'recipient']
