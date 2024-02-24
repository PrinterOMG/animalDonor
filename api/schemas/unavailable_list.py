from datetime import datetime

from pydantic import BaseModel


class UnavailableListBase(BaseModel):
    start_at: datetime
    end_at: datetime


class UnavailableListRead(UnavailableListBase):
    id: int


class UnavailableListCreate(UnavailableListBase):
    pass


class UnavailableListUpdate(UnavailableListBase):
    pass
