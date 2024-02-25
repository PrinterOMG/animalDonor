from pydantic import BaseModel


class SocialNetworkTypeBase(BaseModel):
    name: str


class SocialNetworkTypeRead(SocialNetworkTypeBase):
    id: int
