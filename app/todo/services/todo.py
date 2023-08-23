from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.todo.repositories.todo import TodoRepository
from app.todo.schemas import TodoCreate, TodoUpdate, TodoView


class TodoService(BaseService[TodoCreate, TodoUpdate, TodoView]):
    def __init__(self, db: Session):
        super().__init__(
            repository=TodoRepository,
            db=db,
        )
