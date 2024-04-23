from typing import Annotated, List

from fastapi import Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from models.cell import GetCellDto
from models.sheet import CreateSheetDto, GetSheetInfoDto
from repositories.sheet import SheetRepository
from schemas import Cell
from schemas.sheet import Sheet
from repositories.cell import CellRepository
from errors.exceptions import UnauthorizedException, EntityNotFoundException
from transaction import Transaction

MIN_ORDER = 0
MAX_ORDER = 7


class SheetService:
    db: Session
    sheet_repo: SheetRepository
    cell_repo: CellRepository

    def __init__(self, db: Annotated[Session, Depends(get_db)],
                 sheet_repo: Annotated[SheetRepository, Depends()],
                 cell_repo: Annotated[CellRepository, Depends()],
                 transaction: Annotated[Transaction, Depends()]):
        self.db = db
        self.sheet_repo = sheet_repo
        self.cell_repo = cell_repo
        self.transaction = transaction

    def get_by_user_id(self, user_id: int) -> List[Sheet]:
        return sorted(self.sheet_repo.find_by(owner_id=user_id), key=lambda sheet: sheet.id, reverse=True)

    def create_sheet(self, dto: CreateSheetDto, user_id: int) -> Sheet:
        with self.transaction:
            sheet = Sheet(**dto.dict(), owner_id=user_id)
            cell_1 = Cell(step=1, order=0, sheet=sheet)
            children_1 = []
            for order_2 in range(MIN_ORDER, MAX_ORDER + 1):
                cell_2 = Cell(step=2, order=order_2, sheet=sheet)
                children_2 = []
                for order_3 in range(MIN_ORDER, MAX_ORDER + 1):
                    cell_3 = Cell(step=3, order=order_3, sheet=sheet)
                    children_2.append(cell_3)
                cell_2.children = children_2
                children_1.append(cell_2)
            cell_1.children = children_1
            self.cell_repo.create_or_update(cell_1)
            self.sheet_repo.create_or_update(sheet)
        return sheet

    def get_by_sheet_id(self, sheet_id: int, user_id: int) -> GetSheetInfoDto | None:
        sheet = self.sheet_repo.find_by_id(sheet_id)
        if sheet is None:
            raise EntityNotFoundException(Sheet, id=sheet_id)

        if sheet.owner_id != user_id:
            raise UnauthorizedException()
        if sheet is None:
            return None
        cells = self.cell_repo.find_by(sheet_id=sheet.id, step=1)
        if not cells:
            raise EntityNotFoundException(Cell, sheet_id=sheet.id, step=1)
        step_1_cell = cells.pop()
        step_2_cells = step_1_cell.children
        depth_1_cells = list(step_2_cells)
        depth_1_cells.insert(4, step_1_cell)
        return GetSheetInfoDto(**sheet.__dict__, depth_1_cells=[GetCellDto(**cell.__dict__) for cell in depth_1_cells])
