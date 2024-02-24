from pydantic import BaseModel


class CreateRequestResult(BaseModel):
    link_url: str
