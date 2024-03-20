from typing import Annotated, TypeVar, Generic

from fastapi import Depends
from sqlalchemy.orm import Session

from src.dependencies import get_db

T = TypeVar("T")


class BaseRepository(Generic[T]):
    db: Session

    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def get_by_id(self, entity_id: int) -> T:
        return self.db.query(T).filter(T.id == entity_id).first()

    def delete_by_id(self, entity_id: int) -> None:
        entity = self.db.query(T).filter(T.id == entity_id).first()
        if entity is not None:
            self.db.delete(entity)
