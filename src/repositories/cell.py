from typing import override

from sqlalchemy.orm import selectinload

from repositories.base import BaseRepository, T
from schemas.cell import Cell


class CellRepository(BaseRepository[Cell]):
    @override
    def find_by(self, **kwargs) -> list[Cell]:
        super().validate_kwargs(**kwargs)
        result = self._db.query(Cell).filter_by(**kwargs).options(
            selectinload(Cell.children).selectinload(Cell.children)
        ).all()
        return result
