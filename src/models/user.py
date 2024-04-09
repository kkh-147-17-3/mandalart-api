from pydantic import BaseModel


class BaseUserDto(BaseModel):
    id: int
    social_provider: str


class UserDto(BaseUserDto):
    nickname: str

