from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api import deps
from app.common.exceptions import RecordNotFoundException, RecordNotFoundHTTPException
from app.todo.schemas.todo import TodoCreate, TodoUpdate, TodoView
from app.todo.services.todo import TodoService

router = APIRouter()


@router.post("/", response_model=TodoView)
def create_todo(todo: TodoCreate, service: TodoService = Depends(deps.get_todo_sevice)):
    return service.create(create=todo)


@router.get("/", response_model=List[TodoView])
def get_all_todo(service: TodoService = Depends(deps.get_todo_sevice)):
    return service.get_all()


@router.get("/{id_todo}", response_model=TodoView)
def get_todo_by_id(id_todo: UUID, service: TodoService = Depends(deps.get_todo_sevice)):
    try:
        return service.get_by_id(id_todo=id_todo)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Todo not found")


@router.delete("/{id_todo}")
def delete_todo(id_todo: UUID, service: TodoService = Depends(deps.get_todo_sevice)):
    service.delete(id_todo=id_todo)


@router.put("/{id_todo}", response_model=TodoView)
def update_todo(
    id_todo: UUID, todo_update: TodoUpdate, service: TodoService = Depends(deps.get_todo_sevice)
):
    return service.update(id_todo=id_todo, update=todo_update)
