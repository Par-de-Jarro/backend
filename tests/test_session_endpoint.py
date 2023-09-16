import json

import pytest

from .base_client import BaseClient


class SessionClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="session")


class UserClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="user")


@pytest.fixture
def session_client(client):
    return SessionClient(client)


@pytest.fixture
def user_client(client):
    return UserClient(client)


@pytest.fixture
def user(user_client, session, make_university):
    user_primary_data = {"email": "email@email.com.br", "password": "SEGREDO!"}
    university = make_university()
    session.add(university)
    session.commit()

    data = {
        "name": "Ricardinho",
        "email": user_primary_data["email"],
        "cellphone": "11999999999",
        "document_id": "12345678901",
        "birthdate": "1990-04-13",
        "course": "Ciência da Computação",
        "bio": "Teste",
        "password": user_primary_data["password"],
        "id_university": university.id_university,
    }
    user_client.create(json.dumps(data))

    return user_primary_data


def test_create_session(user, session_client):
    email = user["email"]
    password = user["password"]

    data = {"email": email, "password": password}

    response = session_client.create(json.dumps(data))
    assert response.status_code == 200


def test_create_session_with_nonexistent_user(user, session_client):
    email = "email@gmail.com"
    password = user["password"]

    data = {"email": email, "password": password}

    response = session_client.create(json.dumps(data))
    assert response.status_code == 401
    assert response.json()["detail"] == "User not registered"


def test_create_session_with_wrong_password(user, session_client):
    email = user["email"]
    password = "senhaErrada"

    data = {"email": email, "password": password}

    response = session_client.create(json.dumps(data))
    assert response.status_code == 401
    assert response.json()["detail"] == "Wrong password"
