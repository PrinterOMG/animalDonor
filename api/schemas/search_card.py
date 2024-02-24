from datetime import date, datetime

from pydantic import BaseModel

from api.schemas.pets import PetRead
from api.schemas.users import UserRead


class SearchCardBase(BaseModel):
    description: str | None
    destination_point: str | None
    blood_amount: int | None
    active_until: date | None
    is_active: bool


class SearchCardRead(SearchCardBase):
    id: int

    created_at: datetime

    author: UserRead
    recipient: PetRead


class SearchCardCreate(SearchCardBase):
    # author_id: int  Author id will be substituted automatically from the current user
    recipient_id: int


class SearchCardUpdate(SearchCardBase):
    description: str | None = None
    destination_point: str | None = None
    blood_amount: int | None = None
    active_until: date | None = None
    is_active: bool | None = None

    recipient_id: int | None = None
