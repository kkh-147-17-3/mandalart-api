import datetime
import re

from sqlalchemy import Column, ForeignKey, Integer, DateTime, CheckConstraint, String, orm
from sqlalchemy.orm import relationship, Mapped

from database import Base


class Cell(Base):
    __tablename__ = "cells"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sheet_id = Column(Integer, ForeignKey("sheets.id"))
    sheet = relationship("Sheet")
    goal = Column(String, nullable=False)
    color = Column(String, nullable=False)
    depth = Column(Integer, default=1, nullable=False)
    order = Column(Integer, default=1, nullable=False)
    parent_id = Column(Integer, ForeignKey("cells.id"))
    parent = relationship("Cell", back_populates="children", remote_side=[id])
    children: list["Cell"] = relationship("Cell", back_populates="parent", order_by="Cell.order.asc()", lazy="selectin")
    created_at: Mapped[datetime.datetime] = Column(DateTime, default=datetime.datetime.now)
    modified_at: Mapped[datetime.datetime] = Column(DateTime, onupdate=datetime.datetime.now)

    @orm.validates('depth')
    def validate_depth(self, _, value):
        if not 0 < value < 4:
            raise ValueError(f'Invalid depth {value}')
        return value

    @orm.validates('order')
    def validate_order(self, _, value):
        if value <= 0 or (self.depth > 1 and value >= 9) or (self.depth == 1 and value != 1):
            raise ValueError(f'Invalid order {value}')
        return value

    @orm.validates('color')
    def validate_color(self, _, color):
        p = re.compile('#(([0-9a-fA-F]{2}){3}|([0-9a-fA-F]){3})')

        if not p.match(color):
            raise ValueError(f'Invalid color {color}')
        return color
