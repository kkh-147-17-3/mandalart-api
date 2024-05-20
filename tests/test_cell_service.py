from unittest.mock import patch, MagicMock

import pytest

from models.cell import CreateCellDto, UpdateCellDto
from repositories import CellRepository, SheetRepository
from schemas import Cell, Sheet
from schemas.todo import Todo
from services import CellService
from test_config import mock_db_session
from errors.exceptions import UnauthorizedException, EntityNotFoundException
from transaction import Transaction


@pytest.fixture
def mock_service(mock_db_session):
    cell_repo = CellRepository(mock_db_session)
    sheet_repo = SheetRepository(mock_db_session)
    transaction = Transaction(mock_db_session)
    return CellService(mock_db_session, cell_repo, sheet_repo, transaction)


def mock_create_or_update(cell: Cell):
    if cell.id is None:
        cell.id = 1

    if cell.todos:
        todos = [Todo(owner_id=todo.owner_id, content=todo.content, cell_id=cell.id, id=idx + 1) for idx, todo in
                 enumerate(cell.todos)]
        cell.todos = todos

    for child in cell.children:
        mock_create_or_update(child)

    return None


def test_update_cell_raise_error_when_cell(mock_service):
    mock_cell_repo = MagicMock(spec=CellRepository)
    mock_sheet_repo = MagicMock(spec=CellRepository)

    with (
        patch.object(mock_service, 'cell_repo', mock_cell_repo),
        patch.object(mock_service, 'sheet_repo', mock_sheet_repo),
    ):
        cell_id = 1001
        user_id = 1
        mock_cell_repo.find_by_id.return_value = None
        data = UpdateCellDto(
            goal='test',
            color='ffffffff',
            is_completed=False,
            todos=["test1", "test2"]
        )
        try:
            mock_service.update_cell(data, user_id, cell_id)
            assert False
        except EntityNotFoundException:
            assert True


def test_update_cell_raise_when_owner_is_different(mock_service):
    mock_cell_repo = MagicMock(spec=CellRepository)
    mock_sheet_repo = MagicMock(spec=CellRepository)

    with (
        patch.object(mock_service, 'cell_repo', mock_cell_repo),
        patch.object(mock_service, 'sheet_repo', mock_sheet_repo),
    ):
        cell_id = 1001
        user_id = 1
        mock_cell_repo.find_by_id.return_value = Cell(
            id=cell_id,
            sheet=Sheet(id=1, owner_id=2),
            color='FFFFFFFF',
            is_completed=False,
            todos=[Todo(id=1, cell_id=cell_id, content="test1", owner_id=user_id)]
        )
        data = UpdateCellDto(
            goal='test',
            color='ffffffff',
            is_completed=False,
            todos=["test1", "test2"]
        )
        try:
            mock_service.update_cell(data, user_id, cell_id)
            assert False
        except UnauthorizedException:
            assert True


def test_update_cell_success(mock_service):
    mock_cell_repo = MagicMock(spec=CellRepository)
    mock_sheet_repo = MagicMock(spec=SheetRepository)
    todos = ["test1", "test2"]
    with (
        patch.object(mock_service, 'cell_repo', mock_cell_repo),
    ):
        cell_id = 1001
        user_id = 1
        data = UpdateCellDto(
            goal='test123',
            color='FFAABBAA',
            is_completed=True,
            todos=todos
        )
        original_cell = Cell(
            id=cell_id,
            sheet=Sheet(id=1, owner_id=user_id),
            color='FFFFFFFF',
            is_completed=False
        )
        mock_cell_repo.find_by_id.return_value = original_cell
        # updated_cell = Cell(
        #     id=cell_id,
        #     sheet=Sheet(id=1, owner_id=user_id),
        #     color=data.color,
        #     is_completed=data.is_completed,
        #     goal=data.goal,
        #     todos=[
        #
        #     ]
        # )
        mock_cell_repo.create_or_update.side_effect = mock_create_or_update

        try:
            result = mock_service.update_cell(data, user_id, cell_id)
            assert result.color == data.color
            assert result.is_completed == data.is_completed
            assert result.id == cell_id
            assert result.goal == data.goal
            for idx, todo in enumerate(result.todos):
                assert todo.content == data.todos[idx]

        except UnauthorizedException:
            assert False


def test_get_by_sheet_id_and_depth_and_parent_order(mock_service):
    mock_cell_repo = MagicMock(spec=CellRepository)
    mock_sheet_repo = MagicMock(spec=CellRepository)

    with (
        patch.object(mock_service, 'cell_repo', mock_cell_repo),
        patch.object(mock_service, 'sheet_repo', mock_sheet_repo),
    ):
        sheet_id = 1001
        user_id = 1
        cell_id = 10
        depth = 2
        parent_order = 3

        mock_sheet_repo.find_by_id.return_value = Sheet(id=sheet_id, owner_id=1)
        mock_cell_repo.find_by.return_value = [Cell(
            id=cell_id,
            step=depth,
            order=parent_order,
            is_completed=False,
            children=[Cell(id=i + 100, step=depth + 1, order=i, is_completed=True) for i in range(0, 8)]
        )]

        try:
            result = mock_service.get_by_sheet_id_and_depth_and_parent_order(user_id, sheet_id, depth, parent_order)
            assert result[4].id == cell_id
            assert result[4].step == depth
            assert result[0].id == 100
            assert result[0].step == depth + 1
            assert result[7].id == 106
            assert result[7].step == depth + 1

        except Exception:
            assert False


def test_delete_by_id(mock_service):
    mock_cell_repo = MagicMock(spec=CellRepository)
    mock_transaction = MagicMock(spec=Transaction)

    with (
        patch.object(mock_service, 'cell_repo', mock_cell_repo),
        patch.object(mock_service, 'transaction', mock_transaction)
    ):
        user_id = 1
        cell_id = 10
        depth = 2
        parent_order = 3
        cell = Cell(
            id=cell_id,
            step=depth,
            sheet=Sheet(
                owner_id=user_id
            ),
            order=parent_order,
            is_completed=False,
            children=[Cell(id=i + 100, step=depth + 1, order=i, is_completed=True, goal='test', color='F13231FF') for i
                      in range(0, 8)]
        )
        mock_cell_repo.find_by_id.return_value = cell

        try:
            result = mock_service.delete_cell(user_id, cell_id)
            assert result.goal is None
            assert result.color is None
            assert result.is_completed == False
            assert len(result.todos) == 0
            for child in cell.children:
                assert child.goal is None
                assert child.color is None
                assert child.is_completed is False
                assert child.todos == []

            mock_cell_repo.create_or_update.assert_called_once_with(cell)
            mock_transaction.__enter__.assert_called_once()
            mock_transaction.__exit__.assert_called_once_with(None, None, None)

        except Exception:
            assert False
