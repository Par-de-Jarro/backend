from uuid import UUID

from sqlalchemy.orm import Session

import app.common.models as models
from app.common.repositories.base import BaseRepository


class TodoRepository(BaseRepository[models.Todo, UUID]):
    def __init__(self, db: Session):
        super(TodoRepository, self).__init__(
            models.Todo.id_todo,
            model_class=models.Todo,
            db=db,
        )
