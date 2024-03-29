from unittest.mock import patch, MagicMock

import pytest

from models.cell import CreateCellDto
from repositories import CellRepository
from schemas import Cell, Sheet
from services import CellService
from test_config import mock_db_session
from errors.exceptions import UnauthorizedException


@pytest.fixture
def mock_service(mock_db_session):
    cell_repo = CellRepository(mock_db_session)
    sheet_repo = CellRepository(mock_db_session)
    return CellService(mock_db_session, cell_repo, sheet_repo)


def test_create_cell_raise_error_when_no_parent(mock_service):
    mock_cell_repo = MagicMock(spec=CellRepository)
    mock_sheet_repo = MagicMock(spec=CellRepository)

    with (
        patch.object(mock_service, 'cell_repo', mock_cell_repo),
        patch.object(mock_service, 'sheet_repo', mock_sheet_repo),
        ):
        mock_cell_repo.find_by.side_effect = [None, None]
        mock_sheet_repo.find_by_id.return_value = Sheet(owner_id=1)
        data = CreateCellDto(**{
            'sheet_id': 1,
            'goal': 'test',
            'color': '#fff',
            'step': 2,
            'order': 3,
            'parent_order': 3
        })
        try:
            mock_service.create_cell(data)
            assert False
        except ValueError:
            assert True
        assert mock_cell_repo.find_by.call_count == 2


def test_create_cell_raise_error_already_exists(mock_service):
    mock_cell_repo = MagicMock(spec=CellRepository)
    mock_sheet_repo = MagicMock(spec=CellRepository)

    with (
        patch.object(mock_service, 'cell_repo', mock_cell_repo),
        patch.object(mock_service, 'sheet_repo', mock_sheet_repo),
        ):
        mock_cell_repo.find_by.side_effect = [Cell(step=2,order=3)]
        mock_sheet_repo.find_by_id.return_value = Sheet(owner_id=1)
        data = CreateCellDto(**{
            'sheet_id': 1,
            'goal': 'test',
            'color': '#fff',
            'step': 2,
            'order': 3,
            'parent_order': 3
        })
        try:
            mock_service.create_cell(data)
            assert False
        except ValueError:
            assert True
        assert mock_cell_repo.find_by.call_count == 1


def test_create_cell_raise_error_when_unauthorized(mock_service):
    mock_cell_repo = MagicMock(spec=CellRepository)
    mock_sheet_repo = MagicMock(spec=CellRepository)

    with (
        patch.object(mock_service, 'cell_repo', mock_cell_repo),
        patch.object(mock_service, 'sheet_repo', mock_sheet_repo),
        ):
        mock_cell_repo.find_by.side_effect = [Cell(step=2,order=3)]
        mock_sheet_repo.find_by_id.return_value = Sheet(owner_id=2)
        data = CreateCellDto(**{
            'sheet_id': 1,
            'goal': 'test',
            'color': '#fff',
            'step': 2,
            'order': 3,
            'parent_order': 3
        })
        try:
            mock_service.create_cell(data)
            assert False
        except UnauthorizedException:
            assert True
        assert mock_cell_repo.find_by.call_count == 0