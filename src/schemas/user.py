from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.types import Enum

from database import Base
from enums import SocialProvider


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    social_id = Column(String)
    social_provider = Column(Enum(SocialProvider, native_enum=False))
    sheets = relationship("Sheet", back_populates="owner")
