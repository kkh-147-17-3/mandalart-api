from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from errors.error import UnauthorizedError
from models.cell import CreateCellDto, UpdateCellDto
from repositories import SheetRepository
from repositories.cell import CellRepository
from schemas.cell import Cell


class CellService:
    cell_repo: CellRepository
    sheet_repo: SheetRepository
    db: Session

    def __init__(self,
                 db: Annotated[Session, Depends(get_db)],
                 cell_repo: Annotated[CellRepository, Depends()],
                 sheet_repo: Annotated[SheetRepository, Depends()]
                 ):
        self.db = db
        self.cell_repo = cell_repo
        self.sheet_repo = sheet_repo

    def create_cell(self, dto: CreateCellDto, user_id: int = 1):
        cell = Cell(
            depth=dto.depth,
            order=dto.order,
            goal=dto.goal,
            sheet_id=dto.sheet_id,
            color=dto.color
        )

        sheet = self.sheet_repo.find_by_id(dto.sheet_id)
        if not sheet:
            raise ValueError("sheet not found")

        if sheet.user_id != user_id:
            raise UnauthorizedError()

        if prev_cell := self.cell_repo.find_by(depth=dto.depth, order=dto.order, sheet_id=dto.sheet_id):
            raise ValueError(f"Cell with depth {dto.depth} and order {dto.order} has been already existed")

        if dto.depth > 1:
            parent_cells = self.cell_repo.find_by(depth=dto.depth - 1, sheet_id=dto.sheet_id,
                                                  order=dto.parent_order)
            if not parent_cells:
                raise ValueError("Parent cell not found")
            parent_cell = parent_cells.pop()

            parent_cell.children.append(cell)
            self.db.add(parent_cell)
        else:
            self.db.add(cell)
        self.db.commit()
        return cell

    def update_cell(self, dto: UpdateCellDto, user_id: int, cell_id: int):
        cell = self.cell_repo.find_by_id(cell_id)
        if not cell:
            raise ValueError("cell not found")

        if cell.sheet.owner_id != user_id:
            raise UnauthorizedError()

        cell.color = dto.color if dto.color else cell.color
        cell.goal = dto.goal if dto.goal else cell.goal

        self.db.add(cell)
        self.db.commit()
        return cell
