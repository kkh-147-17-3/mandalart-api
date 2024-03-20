from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm.session import Session

from dependencies import get_db
from schemas import models
from repositories.test import ProductRepository

class ProductService:
    db: Session
    prod_repository: ProductRepository

    def __init__(self, db: Annotated[Session, Depends(get_db)],
                 prod_repository: Annotated[ProductRepository, Depends()]):
        print("서비스 생성됨")
        self.db = db
        self.prod_repository = prod_repository
        pass

    # def __init__(self,
    #              db: Annotated[Session, Depends(get_db)],
    #              product_repository: Annotated[ProductRepository, Depends(ProductRepository)],
    #              ):
    #     print("서비스 생성됨")
    #     self.db = db
    #     self.prod_repository = product_repository

    def get_items(self) -> list[models.Product]:
        print("서비스 호출됨")
        return self.prod_repository.get_items()
