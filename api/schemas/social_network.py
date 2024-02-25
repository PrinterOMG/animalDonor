from datetime import datetime

from pydantic import BaseModel

from api.schemas.social_network_type import SocialNetworkTypeRead


class SocialNetworkBase(BaseModel):
    link: str
    is_public: bool


class SocialNetworkRead(SocialNetworkBase):
    id: int
    created_at: datetime

    social_network_type: SocialNetworkTypeRead


class SocialNetworkCreate(SocialNetworkBase):
    social_network_type_id: int


class SocialNetworkUpdate(SocialNetworkBase):
    social_network_type_id: int
