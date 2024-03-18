from typing import Annotated

from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm.session import Session

from database import get_db
from models import Product
from service.test import ProductService

router = InferringRouter()


@cbv(router)
class UserCBV:
    db: Session = Depends(get_db)
    product_service: ProductService = Depends(ProductService)
    
    @router.get("/user/{user_id}")
    def get_user(self, user_id: int):
        print("호출됨")
        self.db.query(Product).filter(Product.id > 100000)
        return self.product_service.get_items()


