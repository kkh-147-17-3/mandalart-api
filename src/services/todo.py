from typing import Annotated

from fastapi import Depends

from errors.exceptions import EntityNotFoundException, UnauthorizedException
from models.todo import GetTodoDto, CreateTodoDto, UpdateTodoDto
from repositories import TodoRepository, CellRepository
from schemas.todo import Todo
from transaction import Transaction


class TodoService:
    def __init__(self,
                 tx: Annotated[Transaction, Depends()],
                 todo_repository: Annotated[TodoRepository, Depends()],
                 cell_repository: Annotated[CellRepository, Depends()]):
        self.todo_repository = todo_repository
        self.cell_repository = cell_repository
        self.transaction = tx

    def create_todo(self, user_id: int, cell_id: int, create_dto: CreateTodoDto) -> GetTodoDto:
        with self.transaction:
            cell = self.cell_repository.find_by_id(cell_id)
            if not cell:
                raise EntityNotFoundException("Cell not found")
            if cell.owner_id != user_id:
                raise UnauthorizedException()

            todo = Todo(cell=cell, content=create_dto.content, owner_id=user_id)
            self.todo_repository.create_or_update(todo)

        return GetTodoDto.from_orm(todo)

    def update_todo(self, user_id: int, todo_id: int, update_dto: UpdateTodoDto) -> GetTodoDto:
        with self.transaction:
            todo = self.todo_repository.find_by_id(todo_id)
            if not todo:
                raise EntityNotFoundException("Cell not found")
            if todo.owner_id != user_id:
                raise UnauthorizedException()

            todo.content = update_dto.content
            self.todo_repository.create_or_update(todo)
        return GetTodoDto.from_orm(todo)

    def delete_todo(self, user_id: int, todo_id) -> None:
        todo = self.todo_repository.find_by_id(todo_id)
        if not todo:
            raise EntityNotFoundException(msg="Cell not found")
        if todo.owner_id != user_id:
            raise UnauthorizedException()

        with self.transaction:
            self.todo_repository.delete(todo)

    def get_by_user_id_and_cell_id(self, user_id: int, cell_id: int) -> list[GetTodoDto]:
        cell = self.cell_repository.find_by_id(cell_id)
        if not cell:
            raise EntityNotFoundException("Cell not found")
        if cell.owner_id != user_id:
            raise UnauthorizedException()
        todos = cell.todos
        return sorted([GetTodoDto(**todo.__dict__) for todo in todos], reverse=True, key=lambda todo: todo.id)
