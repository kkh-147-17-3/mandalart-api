from pydantic import BaseModel


class ErrorResponse(BaseModel):
    status: int
    message: str
