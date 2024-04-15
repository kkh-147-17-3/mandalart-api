from pydantic import BaseModel


class BaseTodoDto(BaseModel):
    content: str


class GetTodoDto(BaseTodoDto):
    id: int
    cell_id: int

    class Config:
        orm_mode = True


class CreateTodoDto(BaseTodoDto):
    pass


class UpdateTodoDto(BaseTodoDto):
    pass
