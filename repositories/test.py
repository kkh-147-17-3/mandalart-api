from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Product


class ProductRepository:
    db: Session

    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        print("repo 생성됨")
        self.db = db

    def get_items(self):
        print("repo 호출됨")
        return self.db.query(Product).limit(10).all()
