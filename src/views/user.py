from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm.session import Session

from dependencies import get_db
from src.services.test import ProductService
from src.services.test2 import CategoryService

router = InferringRouter()


@cbv(router)
class UserCBV:
    db: Session = Depends(get_db)
    # user_id: int = Depends(get_user_id)
    product_service: ProductService = Depends(ProductService)
    category_service: CategoryService = Depends(CategoryService)

    @router.get("/user/{user_id}")
    def get_user(self, user_id: int):
        return self.product_service.get_items()


