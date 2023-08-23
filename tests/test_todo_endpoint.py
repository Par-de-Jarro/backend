import json

import pytest

from .base_client import BaseClient


class TodoClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="todo")


@pytest.fixture
def todo_client(client):
    return TodoClient(client)


@pytest.fixture
def todo(make_todo):
    return make_todo()


def test_create_todo(todo_client):
    data = {
        "description": "string",
    }
    response = todo_client.create(json.dumps(data))

    assert response.status_code == 200
    assert response.json()["description"] == "string"


@pytest.mark.parametrize(
    "field,expected_field",
    [
        ("description", "new_description"),
    ],
)
def test_update_todo(todo, session, todo_client, field, expected_field):
    session.add(todo)
    session.commit()

    data = {field: expected_field}

    response = todo_client.update(id=todo.id_todo, update=json.dumps(data))
    assert response.status_code == 200
    assert response.json()[field] == expected_field


def test_delete_todo(todo, session, todo_client):
    session.add(todo)
    session.commit()

    todo_client.delete(id=todo.id_todo)
    response = todo_client.get_by_id(id=todo.id_todo)
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_get_todo_by_id(todo, session, todo_client):
    session.add(todo)
    session.commit()
    response = todo_client.get_by_id(id=todo.id_todo)

    assert response.status_code == 200
    assert response.json()["id_todo"] == str(todo.id_todo)
    assert response.json()["description"] == str(todo.description)


def test_list_todo(todo, session, todo_client):
    session.add(todo)
    session.commit()
    response = todo_client.get_all()

    assert response.status_code == 200
    assert len(response.json()) == 1
