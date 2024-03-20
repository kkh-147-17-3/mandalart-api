from .base import BaseRepository
from schemas import models

Product = models.Product


class ProductRepository(BaseRepository):

    def get_items(self):
        return self.db.query(Product).limit(10).all()
