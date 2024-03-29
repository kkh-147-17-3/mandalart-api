from datetime import datetime

from pydantic import BaseModel

from models.cell import GetCellWithChildrenDto, GetCellDto


class GetSheetDto(BaseModel):
    id: int
    owner_id: int
    name: str
    created_at: datetime
    modified_at: datetime | None

    class Config:
        orm_mode = True


class CreateSheetDto(BaseModel):
    name: str


class GetSheetInfoDto(GetSheetDto):
    """
    step_1_cell: 만다르트의 가장 정중앙에 위치한 셀을 의미합니다.
    """
    depth_1_cells: list[GetCellDto]
