from typing import TypeVar, Generic

from pydantic.generics import GenericModel

T = TypeVar('T')


class GenericResponse(GenericModel, Generic[T]):
    status: int
    data: T
    message: str | None
