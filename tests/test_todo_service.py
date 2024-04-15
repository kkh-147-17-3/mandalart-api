from unittest.mock import patch, MagicMock

import pytest

from models.todo import CreateTodoDto, UpdateTodoDto
from repositories import CellRepository, TodoRepository
from schemas import Cell, Sheet
from schemas.todo import Todo
from services.todo import TodoService
from test_config import mock_db_session
from transaction import Transaction


@pytest.fixture
def mock_service(mock_db_session):
    todo_repo = TodoRepository(mock_db_session)
    cell_repo = CellRepository(mock_db_session)
    transaction = Transaction(mock_db_session)
    return TodoService(transaction, todo_repo, cell_repo)


def mock_create_or_update(todo: Todo):
    if todo.id is None:
        todo.id = 1

    if todo.cell is not None and todo.cell_id is None:
        todo.cell_id = todo.cell.id

    return todo


def test_create_todo(mock_service):
    user_id = 1
    cell_id = 2
    content = "test content"

    create_dto = CreateTodoDto(**{
        "content": content
    })

    mock_todo_repo = MagicMock(spec=TodoRepository)
    mock_cell_repo = MagicMock(spec=CellRepository)
    mock_cell_repo.find_by_id.return_value = Cell(
        id=cell_id,
        owner_id=user_id,
        sheet=Sheet(
            id=1,
            owner_id=user_id
        )
    )
    mock_todo_repo.create_or_update.side_effect = mock_create_or_update
    with (
        patch.object(mock_service, 'todo_repository', mock_todo_repo),
        patch.object(mock_service, 'cell_repository', mock_cell_repo),
    ):
        todo = mock_service.create_todo(user_id, cell_id, create_dto)
        assert todo.content == content
        assert todo.cell_id == cell_id
        assert todo.id is not None


def test_update_todo(mock_service):
    user_id = 1
    todo_id = 2
    cell_id = 1
    content = "update test content"
    update_dto = UpdateTodoDto(**{
        "id": todo_id,
        "content": content
    })
    mock_todo_repo = MagicMock(spec=TodoRepository)
    mock_todo_repo.find_by_id.return_value = Todo(
        id=todo_id,
        owner_id=user_id,
        cell_id=cell_id
    )
    mock_todo_repo.create_or_update.side_effect = mock_create_or_update
    with patch.object(mock_service, "todo_repository", mock_todo_repo):
        updated_todo = mock_service.update_todo(user_id, todo_id, update_dto)
        assert updated_todo.content == content
        assert updated_todo.id == todo_id


def test_get_by_user_id_and_cell_id(mock_service):
    user_id = 1
    cell_id = 2
    mock_cell_repo = MagicMock(spec=CellRepository)
    mock_cell_repo.find_by_id.return_value = Cell(
        id=cell_id,
        owner_id=user_id,
        todos=[
            Todo(
                id=1,
                owner_id=user_id,
                cell_id=cell_id,
                content="test 123"
            ),
            Todo(
                id=2,
                owner_id=user_id,
                cell_id=cell_id,
                content="test 456"
            )
        ]
    )
    with patch.object(mock_service, "cell_repository", mock_cell_repo):
        todos = mock_service.get_by_user_id_and_cell_id(user_id, cell_id)
        assert len(todos) == 2
        assert todos[0].id == 2
        assert todos[1].id == 1
        assert todos[0].cell_id == todos[1].cell_id == cell_id
