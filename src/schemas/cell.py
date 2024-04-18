import datetime
import re

from sqlalchemy import Column, ForeignKey, Integer, DateTime, CheckConstraint, String, orm, Boolean
from sqlalchemy.orm import relationship, Mapped

from database import Base
from schemas.todo import Todo


class Cell(Base):
    __tablename__ = "cells"
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")
    sheet_id = Column(Integer, ForeignKey("sheets.id"))
    sheet = relationship("Sheet")
    todos: Mapped[list[Todo]] = relationship("Todo", back_populates="cell")
    goal = Column(String, nullable=True)
    color = Column(String, nullable=True)
    step = Column(Integer, default=1, nullable=False)
    order = Column(Integer, default=1, nullable=False)
    parent_id = Column(Integer, ForeignKey("cells.id"))
    parent = relationship("Cell", back_populates="children", remote_side=[id])
    is_completed = Column(Boolean, default=False, nullable=False)
    children: Mapped[list["Cell"]] = relationship("Cell", back_populates="parent", order_by="Cell.order.asc()",
                                                  lazy="selectin")
    created_at: Mapped[datetime.datetime] = Column(DateTime, default=datetime.datetime.now)
    modified_at: Mapped[datetime.datetime] = Column(DateTime, onupdate=datetime.datetime.now)

    @orm.validates('step')
    def validate_step(self, _, value):
        if not 0 < value < 4:
            raise ValueError(f'Invalid step {value}')
        return value

    @orm.validates('order')
    def validate_order(self, _, value):
        if value < 0 or (self.step > 1 and value >= 8) or (self.step == 1 and value != 0):
            raise ValueError(f'Invalid order {value}')
        return value

    @orm.validates('color')
    def validate_color(self, _, color):
        p = re.compile('([0-9a-fA-F]{2}){4}')

        if not p.match(color):
            raise ValueError(f'Invalid color {color}')
        return color
