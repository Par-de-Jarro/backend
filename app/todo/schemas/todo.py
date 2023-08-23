from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TodoBase(BaseModel):
    description: str


class TodoCreate(TodoBase):
    ...


class TodoView(TodoBase):
    id_todo: UUID

    class Config:
        orm_mode = True


class TodoUpdate(BaseModel):
    description: Optional[str]
