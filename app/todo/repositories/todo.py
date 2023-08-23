from uuid import UUID

from sqlalchemy.orm import Session

from app.common.models.todo import Todo
from app.common.repositories.base import BaseRepository


class TodoRepository(BaseRepository[Todo, UUID]):
    def __init__(self, db: Session):
        super(TodoRepository, self).__init__(
            Todo.id_todo,
            model_class=Todo,
            db=db,
        )
