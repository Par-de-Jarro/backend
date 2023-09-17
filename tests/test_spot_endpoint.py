import json
from uuid import UUID

import pytest

from app.api.deps import get_id_user_by_auth_token
from app.main import app

from .base_client import BaseClient


async def override_id_user(id_user: UUID):
    return id_user


class SpotClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="spot")

    def update(self, update):
        return self.client.put(f"/{self.path}/", data=update, headers=self.headers)

    def delete(self):
        return self.client.delete(f"/{self.path}/", headers=self.headers)


@pytest.fixture
def spot_client(client):
    return SpotClient(client)


@pytest.fixture
def spot(make_spot):
    return make_spot()


@pytest.fixture
def user(make_user):
    return make_user()


def test_create_spot(spot_client, spot, user, fastapi_dep, session):
    session.add(spot)
    session.commit()

    with fastapi_dep(app).override({get_id_user_by_auth_token: user.id_user}):
        data = {
            "name": "Spot Teste",
            "description": "Teste",
            "lat": -7.216306580255391,
            "long": -35.909625553967125,
        }

    response = spot_client.create(json.dumps(data), id_user=user.id_user)
    assert response.status_code == 200
    assert response.json()["name"] == "Spot Teste"
    assert response.json()["description"] == "Teste"


def test_get_all_spot(spot_client, spot, session):
    session.add(spot)
    session.commit()

    response = spot_client.get_all()
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Spot Teste"
    assert response.json()[0]["description"] == "Teste"


def test_search_spot(spot_client, spot, session):
    session.add(spot)
    session.commit()

    response = spot_client.search()
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Spot Teste"
    assert response.json()[0]["description"] == "Teste"


def test_get_by_id_spot(spot_client, spot, session):
    session.add(spot)
    session.commit()

    response = spot_client.get_by_id(spot.id_spot)
    assert response.status_code == 200
    assert response.json()["name"] == "Spot Teste"
    assert response.json()["description"] == "Teste"


@pytest.mark.parametrize(
    "field,expected_field",
    [("name", "Novo nome"), ("description", "Teste")],
)
def test_update_spot(fastapi_dep, spot, session, spot_client, field, expected_field):
    session.add(spot)
    session.commit()

    with fastapi_dep(app).override({get_id_user_by_auth_token: spot.id_spot}):
        data = {field: expected_field}

        response = spot_client.update(update=json.dumps(data))
        assert response.status_code == 200
        assert response.json()[field] == expected_field


def test_delete_spot(spot, fastapi_dep, session, spot_client):
    session.add(spot)
    session.commit()

    with fastapi_dep(app).override({get_id_user_by_auth_token: spot.id_spot}):
        spot_client.delete()
        response = spot_client.get_by_id(id=spot.id_spot)
        assert response.status_code == 404
        assert response.json()["detail"] == "Spot not found"
