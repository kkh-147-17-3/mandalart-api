import datetime
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship, Mapped

from database import Base


class Sheet(Base):
    __tablename__ = "sheets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="sheets")
    name = Column(String)
    created_at: Mapped[datetime.datetime] = Column(DateTime, default=datetime.datetime.now)
    modified_at: Mapped[datetime.datetime] = Column(DateTime, onupdate=datetime.datetime.now)