from pydantic import BaseModel


class BaseTokenDto(BaseModel):
    access_token: str
    refresh_token: str
