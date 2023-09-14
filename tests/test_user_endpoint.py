import json
import uuid

import pytest

from .base_client import BaseClient


class UserClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="user")


@pytest.fixture
def user_client(client):
    return UserClient(client)


@pytest.fixture
def user(make_user):
    return make_user()


def test_create_user(user_client):
    data = {
        "name": "Ricardinho",
        "email": "teste@email.com",
        "cellphone": "11999999999",
        "document_id": "12345678901",
        "birthdate": "1990-04-13",
        "course": "Ciência da Computação",
        "bio": "Teste",
        "password": "123456",
    }

    response = user_client.create(json.dumps(data))
    assert response.status_code == 200
    assert response.json()["name"] == "Ricardinho"
    assert response.json()["course"] == "Ciência da Computação"


@pytest.mark.parametrize(
    "field,expected_field",
    [("name", "Novo nome"), ("cellphone", "11888888888"), ("document_id", "12312312312")],
)
def test_update_user(user, session, user_client, field, expected_field):
    session.add(user)
    session.commit()

    data = {field: expected_field}

    response = user_client.update(id=user.id_user, update=json.dumps(data))
    assert response.status_code == 200
    assert response.json()[field] == expected_field


def test_delete_user(user, session, user_client):
    session.add(user)
    session.commit()

    user_client.delete(id=user.id_user)
    response = user_client.get_by_id(id=user.id_user)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_user_by_id(user, session, user_client):
    session.add(user)
    session.commit()
    response = user_client.get_by_id(id=user.id_user)
    assert response.status_code == 200
    assert response.json()["name"] == "Ricardinho"
    assert response.json()["course"] == "Ciência da Computação"


def test_list_user(user, session, user_client):
    session.add(user)
    session.commit()
    response = user_client.get_all()
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.parametrize(
    "field,expected_field",
    [("name", "Novo nome"), ("cellphone", "11888888888"), ("document_id", "12312312312")],
)
def test_update_user_with_user_not_found(user_client, field, expected_field):
    data = {field: expected_field}
    user_client.update(id=uuid.uuid4(), update=json.dumps(data))
    response = user_client.get_by_id(id=uuid.uuid4())
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_user_with_user_not_found(user_client):
    user_client.delete(id=uuid.uuid4())
    response = user_client.get_by_id(id=uuid.uuid4())
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_user_by_id_with_user_not_found(user_client):
    response = user_client.get_by_id(id=uuid.uuid4())
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
