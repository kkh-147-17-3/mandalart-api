import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship, Mapped

from database import Base


class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    cell_id = Column(Integer, ForeignKey("cells.id"))
    cell = relationship("Cell")
    content = Column(String)
    created_at: Mapped[datetime.datetime] = Column(DateTime, default=datetime.datetime.now)
    modified_at: Mapped[datetime.datetime] = Column(DateTime, onupdate=datetime.datetime.now)