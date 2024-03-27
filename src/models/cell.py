import re
from typing import List, Self, Optional

from pydantic import BaseModel, Field, validator


class BaseCellDto(BaseModel):
    """
    depth: 1(정중앙), 2(정중앙에서 주위 8 개),3(depth=2 8개 셀 주변에 있는 8개의 셀)\n
    order \n
    |1|2|3|\n
    |4|X|5|\n
    |6|7|8|\n
    """
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
    color: str
    goal: str
    children: list["GetCellWithChildrenDto"]

    class Config:
        orm_mode = True


class UpdateCellDto(BaseModel):
    goal: str
    color: str

    @validator('color')
    def validate_color(cls, color):
        p = re.compile('#(([0-9a-fA-F]{2}){3}|([0-9a-fA-F]){3})')

        if not p.match(color):
            raise ValueError(f'Invalid color {color}')

        return color
