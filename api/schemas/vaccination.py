from datetime import datetime

from pydantic import BaseModel


class VaccinationBase(BaseModel):
    name: str
    active_until: datetime | None


class VaccinationCreate(VaccinationBase):
    pass


class VaccinationRead(VaccinationBase):
    id: int
    created_at: datetime


class VaccinationUpdate(VaccinationBase):
    pass
