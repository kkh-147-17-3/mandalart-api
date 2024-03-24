from datetime import datetime

from pydantic import BaseModel

from models.cell import GetCellWithChildrenDto


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
    depth_1_cell: GetCellWithChildrenDto
