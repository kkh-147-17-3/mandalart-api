from typing import Annotated, TypeVar, Generic, get_args

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base

from database import Base
from dependencies import get_db

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    _db: Session
    __model: Base

    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self._db = db
        self.__model = (get_args(self.__orig_bases__[0])[0])  # type: ignore

    def find_by_id(self, entity_id: int) -> T | None:
        return self._db.query(self.__model).filter(self.__model.id == entity_id).first()

    def create_or_update(self, entity: T) -> T:
        self._db.add(entity)
        return entity

    def delete(self, entity: T) -> None:
        self._db.delete(entity)

    def delete_by_id(self, entity_id: int) -> None:
        entity = self._db.query().filter(self.__model.id == entity_id).first()
        if entity is not None:
            self.delete(entity)

    def validate_kwargs(self, **kwargs):
        for k, v in kwargs.items():
            if not hasattr(self.__model, k):
                raise ValueError(f"field name {k} is not a valid for entity the {self.__model.__name__}")
        return

    def find_by(self, **kwargs) -> list[T]:
        self.validate_kwargs(**kwargs)

        query = self._db.query(self.__model)
        for k, v in kwargs.items():
            query = query.filter(getattr(self.__model, k) == v)

        return query.all()
