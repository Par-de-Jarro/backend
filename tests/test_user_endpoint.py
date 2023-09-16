import json
from uuid import UUID

import pytest

from app.api.deps import get_id_user_by_auth_token
from app.main import app

from .base_client import BaseClient


async def override_id_user(id_user: UUID):
    return id_user


class UserClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="user")

    def update(self, update):
        return self.client.put(f"/{self.path}/", data=update, headers=self.headers)

    def delete(self):
        return self.client.delete(f"/{self.path}/", headers=self.headers)


@pytest.fixture
def user_client(client):
    return UserClient(client)


@pytest.fixture
def user(make_user):
    return make_user()


def test_create_user(user_client, session, make_university):
    university = make_university()
    session.add(university)
    session.commit()

    data = {
        "name": "Ricardinho",
        "email": "teste@email.com",
        "cellphone": "11999999999",
        "document_id": "12345678901",
        "birthdate": "1990-04-13",
        "course": "Ciência da Computação",
        "bio": "Teste",
        "password": "123456",
        "id_university": university.id_university,
    }

    response = user_client.create(json.dumps(data))
    assert response.status_code == 200
    assert response.json()["name"] == "Ricardinho"
    assert response.json()["course"] == "Ciência da Computação"


@pytest.mark.parametrize(
    "field,expected_field",
    [("name", "Novo nome"), ("cellphone", "11888888888"), ("document_id", "12312312312")],
)
def test_update_user(fastapi_dep, user, session, user_client, field, expected_field):
    session.add(user)
    session.commit()

    with fastapi_dep(app).override({get_id_user_by_auth_token: user.id_user}):
        data = {field: expected_field}

        response = user_client.update(update=json.dumps(data))
        assert response.status_code == 200
        assert response.json()[field] == expected_field


def test_delete_user(user, fastapi_dep, session, user_client):
    session.add(user)
    session.commit()

    with fastapi_dep(app).override({get_id_user_by_auth_token: user.id_user}):
        user_client.delete()
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
