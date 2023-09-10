import json

import pytest

from app.user.models.user import User

from .base_client import BaseClient


class UserClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="user")


@pytest.fixture
def user_client(client):
    return UserClient(client)


@pytest.fixture
def make_user():
    data = {
        "name": "Ricardinho",
        "email": "teste@email.com",
        "cellphone": "11999999999",
        "document_id": "12345678901",
        "birthdate": "1990-04-13",
        "course": "Ciência da Computação",
        "bio": "Teste",
        "password": "123456",
        "password_hash": "123456",
    }
    return data


@pytest.fixture
def user(make_user):
    return make_user


def test_create_user(user_client):
    user_data = make_user()
    response = user_client.create(json.dumps(user_data))
    assert response.status_code == 200
    assert response.json()["name"] == "Ricardinho"
    assert response.json()["email"] == "teste@email.com"
    assert response.json()["cellphone"] == "11999999999"
    assert response.json()["document_id"] == "12345678901"
    assert response.json()["birthdate"] == "1990-04-13"
    assert response.json()["course"] == "Ciência da Computação"
    assert response.json()["bio"] == "Teste"


def test_update_user(user, session, user_client):
    user_obj = User(
        name=user["name"],
        email=user["email"],
        cellphone=user["cellphone"],
        document_id=user["document_id"],
        birthdate=user["birthdate"],
        course=user["course"],
        bio=user["bio"],
    )
    session.add(user_obj)
    session.commit()
    data = {
        "name": "Ricardinho",
        "email": "teste@email.com",
        "cellphone": "11999999999",
        "document_id": "12345678901",
        "birthdate": "1999-04-13",
        "course": "Ciência da Computação",
        "bio": "eita como tem bio",
    }
    response = user_client.update(user.id_user, json.dumps(data))
    assert response.status_code == 200
    assert response.json()["birthdate"] == "1999-04-13"
    assert response.json()["bio"] == "eita como tem bio"


def test_delete_user(user, session, user_client):
    user_obj = User(
        name=user["name"],
        email=user["email"],
        cellphone=user["cellphone"],
        document_id=user["document_id"],
        birthdate=user["birthdate"],
        course=user["course"],
        bio=user["bio"],
    )
    session.add(user_obj)
    session.commit()
    response = user_client.delete(user.id_user)
    assert response.status_code == 200


def test_delete_user_not_exists(user, session, user_client):
    user_obj = User(
        name=user["name"],
        email=user["email"],
        cellphone=user["cellphone"],
        document_id=user["document_id"],
        birthdate=user["birthdate"],
        course=user["course"],
        bio=user["bio"],
    )
    session.add(user_obj)
    session.commit()
    response = user_client.delete("123456789")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_user_by_id(user, session, user_client):
    user_obj = User(
        name=user["name"],
        email=user["email"],
        cellphone=user["cellphone"],
        document_id=user["document_id"],
        birthdate=user["birthdate"],
        course=user["course"],
        bio=user["bio"],
    )
    session.add(user_obj)
    session.commit()
    response = user_client.get(user.id_user)
    assert response.status_code == 200
    assert response.json()["name"] == user.name
    assert response.json()["email"] == user.email
    assert response.json()["cellphone"] == user.cellphone
    assert response.json()["document_id"] == user.document_id
    assert response.json()["birthdate"] == user.birthdate
    assert response.json()["course"] == user.course
    assert response.json()["bio"] == user.bio


def test_list_users(user, session, user_client):
    user_obj = User(
        name=user["name"],
        email=user["email"],
        cellphone=user["cellphone"],
        document_id=user["document_id"],
        birthdate=user["birthdate"],
        course=user["course"],
        bio=user["bio"],
    )
    session.add(user_obj)
    session.commit()
    response = user_client.list()
    assert response.status_code == 200
    assert len(response.json()) == 1
