import json

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
        "password_hash": "123456",
    }
    response = user_client.create(json.dumps(data))
    assert response.status_code == 200
    assert response.json()["name"] == "Ricardinho"
    assert response.json()["course"] == "Ciência da Computação"


@pytest.mark.parametrize(
    "field,expected_field",
    [("birthdate", "1999-04-13")],
)
def test_update_user(user, session, user_client, field, expected_field):
    session.add(user)
    session.commit()
    data = {field: expected_field}
    response = user_client.update(user.id_user, json.dumps(data))
    assert response.status_code == 200
    assert response.json()[field] == expected_field


# def test_delete_user(user, session, user_client):
#    session.add(user)
#    session.commit()
#    response = user_client.delete(user.id_user)
#    assert response.status_code == 200
#    assert response.json()["message"] == "User deleted successfully"


def test_get_user_by_id(user, session, user_client):
    session.add(user)
    session.commit()
    response = user_client.get_all(document_id=user.id_user)
    assert response.status_code == 200
    assert response.json()["name"] == "Ricardinho"
    assert response.json()["course"] == "Ciência da Computação"


def test_list_user(user, session, user_client):
    session.add(user)
    session.commit()
    response = user_client.get_all()
    assert response.status_code == 200
    assert len(response.json()) == 1
