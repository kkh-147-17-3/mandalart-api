from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from dependencies import get_db


class Transaction:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.db.rollback()
            return False
        self.db.commit()
        return True
