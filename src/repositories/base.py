from typing import Annotated, TypeVar, Generic

from fastapi import Depends
from sqlalchemy.orm import Session

from src.dependencies import get_db

T = TypeVar("T")


class BaseRepository(Generic[T]):
    db: Session

    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def find_by_id(self, entity_id: int) -> T:
        return self.find_by(id=entity_id).pop()

    def delete_by_id(self, entity_id: int) -> None:
        entity = self.db.query(T).filter(T.id == entity_id).first()
        if entity is not None:
            self.db.delete(entity)

    def find_by(self, **kwargs) -> list[T]:

        query = self.db.query(T)
        for k, v in kwargs.items():
            if hasattr(T, k):
                query = query.filter(T.k == v)
            else:
                raise ValueError(f"field name {k} is not a valid for entity the {T.__class__.__name__}")



        return query.all()