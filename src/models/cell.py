import re
from typing import List, Self, Optional

from pydantic import BaseModel, Field, validator


def validate_color(cls, color: str) -> str:
    p = re.compile('([0-9a-fA-F]{2}){4}')

    if not p.match(color):
        raise ValueError(f'Invalid color {color}')

    return color.upper()


class BaseCellDto(BaseModel):
    """
    step: 1(정중앙), 2(정중앙에서 주위 8 개),3(step=2 8개 셀 주변에 있는 8개의 셀)\n
    order \n
    |1|2|3|\n
    |4|X|5|\n
    |6|7|8|\n
    """
    step: int = Field(None, ge=1, le=3)
    # order: int = Field(None, ge=0, le=7)


class CreateCellDto(BaseCellDto):
    sheet_id: int
    goal: str
    color: str
    parent_order: int | None = None
    _validate_color = validator('color', allow_reuse=True)(validate_color)


class GetCellDto(BaseCellDto):
    id: int
    color: str | None
    goal: str | None
    is_completed: bool

    # parent: Optional["GetCellDto"]

    class Config:
        orm_mode = True


class GetCellWithChildrenDto(BaseCellDto):
    id: int
    color: str | None
    goal: str | None
    is_completed: bool
    children: list[GetCellDto]

    class Config:
        orm_mode = True


class UpdateCellDto(BaseModel):
    goal: str | None = Field(None, description='목표 내용')
    color: str | None = Field(None, description='#을 제외한 셀 색상 hex code 8자리(ex: FFFFFFFF)')
    is_completed: bool | None = Field(None, description='목표 완료 여부')
    _validate_color = validator('color', allow_reuse=True)(validate_color)

    class Config:
        schema_extra = {
            "examples": [{
                "goal": "만다르트 테스트 목표",
                "color": "FFAABB00",
                "is_completed": False
            }]
        }