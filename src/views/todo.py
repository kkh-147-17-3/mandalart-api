from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from models.todo import CreateTodoDto, UpdateTodoDto, GetTodoDto
from services.todo import TodoService
from views.auth import AuthView

router = InferringRouter()


@cbv(router)
class TodoView(AuthView):
    todo_service: TodoService = Depends(TodoService)

    @router.get("/cell/{cell_id}/todo", tags=["todo"], summary="cell 하나의 해야할 일 목록을 불러옵니다.")
    def get_cell_todos(self, cell_id: int) -> list[GetTodoDto]:
        todos = self.todo_service.get_by_user_id_and_cell_id(user_id=self.user_id, cell_id=cell_id)
        return todos

    @router.post("/cell/{cell_id}/todo", tags=["todo"])
    def create_cell_todo(self, cell_id: int, dto: CreateTodoDto) -> GetTodoDto:
        todo = self.todo_service.create_todo(self.user_id, cell_id, dto)
        return todo

    @router.delete("/todo/{todo_id}", tags=["todo"])
    def delete_todo(self, todo_id: int) -> None:
        self.todo_service.delete_todo(self.user_id, todo_id)
        return None

    @router.patch("/todo/{todo_id}", tags=["todo"])
    def update_todo(self, todo_id: int, dto: UpdateTodoDto) -> GetTodoDto:
        updated_todo = self.todo_service.update_todo(self.user_id, todo_id, dto)
        return updated_todo
