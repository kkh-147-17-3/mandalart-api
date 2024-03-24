from typing import Annotated, List

from fastapi import Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from models.sheet import CreateSheetDto, GetSheetInfoDto
from repositories.sheet import SheetRepository
from schemas.sheet import Sheet
from repositories.cell import CellRepository
from errors.error import UnauthorizedError


class SheetService:
    db: Session
    sheet_repo: SheetRepository
    cell_repo: CellRepository

    def __init__(self, db: Annotated[Session, Depends(get_db)], sheet_repo: Annotated[SheetRepository, Depends()],
                 cell_repo: Annotated[CellRepository, Depends()]):
        self.db = db
        self.sheet_repo = sheet_repo
        self.cell_repo = cell_repo

    def get_by_user_id(self, user_id: int) -> List[Sheet]:
        return self.sheet_repo.find_by(owner_id=user_id)

    def create_sheet(self, dto: CreateSheetDto, user_id: int):
        sheet = Sheet(**dto.dict(), owner_id=user_id)
        self.db.add(sheet)
        self.db.commit()
        return sheet

    def get_by_sheet_id(self, sheet_id: int, user_id: int) -> GetSheetInfoDto | None:
        sheet = self.sheet_repo.find_by_id(sheet_id)
        if sheet.owner_id != user_id:
            raise UnauthorizedError()
        if sheet is None:
            return None
        top_cell = self.cell_repo.find_by(sheet_id=sheet.id, depth=1).pop()
        return GetSheetInfoDto(**sheet.__dict__, depth_1_cell=top_cell)
