from typing import TypeVar, Generic, Any, Dict

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar('T')


class GenericResponse(GenericModel, Generic[T]):
    status: int
    data: T
    message: str | None


class ErrorResponse(BaseModel):
    status: int
    data: Dict[str, Any]
    message: str
