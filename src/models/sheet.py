from datetime import datetime

from pydantic import BaseModel

from models.cell import GetCellDto


class GetSheetDto(BaseModel):
    id: int
    owner_id: int
    name: str
    created_at: datetime
    modified_at: datetime | None

    class Config:
        orm_mode = True
        schema_extra = {
            "examples": [{
                "id": 1,
                "owner_id": 1,
                "name": "NAME",
                "created_at": "2024-01-01 12:00:00",
                "modified_at": "2024-01-01 12:00:00",
            }]
        }


class CreateSheetDto(BaseModel):
    name: str


class GetSheetInfoDto(GetSheetDto):
    """
    step_1_cell: 만다르트의 가장 정중앙에 위치한 셀을 의미합니다.
    """
    depth_1_cells: list[GetCellDto]
