import re
from typing import List, Self, Optional

from pydantic import BaseModel, Field, validator


class BaseCellDto(BaseModel):
    depth: int = Field(None, ge=1, le=3)
    order: int = Field(None, ge=1, le=8)


class CreateCellDto(BaseCellDto):
    sheet_id: int
    goal: str
    color: str
    parent_order: int | None = None

    @validator('color')
    def validate_color(cls, color):
        p = re.compile('#(([0-9a-fA-F]{2}){3}|([0-9a-fA-F]){3})')

        if not p.match(color):
            raise ValueError(f'Invalid color {color}')

        return color


class GetCellDto(BaseCellDto):
    id: int
    color: str
    goal: str
    parent: Optional["GetCellDto"]

    class Config:
        orm_mode = True


class GetCellWithChildrenDto(BaseCellDto):
    id: int
    children: list["GetCellWithChildrenDto"]

    class Config:
        orm_mode = True
