from pydantic import BaseModel


class CreateSheetResponse(BaseModel):
    sheet_id: int


class ErrorResponse(BaseModel):
    status: int
    message: str
