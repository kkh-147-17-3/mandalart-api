from dataclasses import dataclass
import datetime
from typing import Tuple, List
import enum

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, BigInteger, Column
from sqlalchemy.orm import relationship, Mapped
from database import Base


# 참고용
class Marketplace(enum.Enum):
    KAKAO = "KAKAO"
    A29CM = "A29CM"
    NAVER = "NAVER"
    OLIVEYOUNG = "OLIVEYOUNG"


def callable_func(obj):
    a = [str(e.value) for e in obj]
    return a


class ProductCategory(Base):
    __tablename__ = "product_category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(ForeignKey("product.id"))
    product = relationship("Product", back_populates="categories")
    shopping_category_id = Column(ForeignKey("naver_shopping_category.id"))
    naver_shopping_category = relationship("NaverShoppingCategory")


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String)
    brand_name: Mapped[str] = Column(String)
    categories: Mapped[List[ProductCategory]] = relationship(ProductCategory, back_populates="product")
    price: Mapped[str] = Column(Integer)
    thumbnail_img_url: Mapped[str] = Column(String)
    buying_url: Mapped[str] = Column(String)
    marketplace: Mapped[Marketplace] = Column(
        Enum(Marketplace, values_callable=callable_func, native_enum=False))
    marketplace_product_id: Mapped[int] = Column(BigInteger)
    review_count: Mapped[int] = Column(Integer)
    like_count: Mapped[int] = Column(Integer)
    overall_rate: Mapped[int] = Column(Integer)
    free_shipping: Mapped[bool] = Column(Boolean, default=False)
    is_sold_out: Mapped[bool] = Column(Boolean, default=False)
    created_at: Mapped[datetime.datetime] = Column(DateTime, default=datetime.datetime.utcnow)
    modified_at: Mapped[datetime.datetime] = Column(DateTime, onupdate=datetime.datetime.utcnow)


class NaverShoppingCategory(Base):
    __tablename__ = "naver_shopping_category"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = Column(String)
    image_url: Mapped[str] = Column(String, nullable=True)
    parent_category_id: Mapped[int] = Column(Integer, ForeignKey("naver_shopping_category.id"))
    parent_category: Mapped["NaverShoppingCategory"] = relationship("NaverShoppingCategory",
                                                                    back_populates="child_categories", remote_side=[id])
    child_categories: Mapped[List["NaverShoppingCategory"]] = relationship("NaverShoppingCategory",
                                                                           back_populates="parent_category")


@dataclass
class NaverShoppingProduct:
    idx: int
    product_id: int
    img_src: str
    title: str
    price: int
    brand_name: str
    categories: Tuple[NaverShoppingCategory, NaverShoppingCategory]
    free_shipping: bool
    score_rate: int
    review_count: int


@dataclass
class ShoppingCategory:
    parent_category_id: int | None
    category_id: int
    category_name: str
