import json
from unittest.mock import patch
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_id_user_by_auth_token
from app.main import app

from .base_client import BaseClient

client = TestClient(app)


async def override_id_user(id_user: UUID):
    return id_user


class SpotClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="spot")

    def search(self):
        return self.client.delete(f"/{self.path}/search", headers=self.headers)


@pytest.fixture
def spot_client(client):
    return SpotClient(client)


@pytest.fixture
def spot(make_spot):
    return make_spot()


@pytest.fixture
def user(make_user):
    return make_user()


def test_create_spot(spot_client, user, fastapi_dep, session):
    session.add(user)
    session.commit()

    spot_body = {
        "name": "Casa Teste",
        "description": "Casa de Teste",
        "personal_quota": 10,
        "type": "house",
        "value": 200,
        "street": "Avenida de Testes",
        "zip_code": "58434500",
        "number": "5255",
        "complement": "B20",
        "city": "Campina Grande",
        "state": "PB",
        "key": {
            "convenience": {"rooms_quantity": 0, "bathrooms_quantity": 0, "has_elevator": True},
            "allowance": {"allow_pet": True, "allow_smoker": True},
        },
    }

    with fastapi_dep(app).override({get_id_user_by_auth_token: user.id_user}):
        with patch(
            "app.common.repositories.google_address_api.GoogleAddressApi.get_location_coordinates",
            return_value=(10, 20),
        ) as mocked_method:
            response = spot_client.create(
                json.dumps(spot_body),
            )

            mocked_method.assert_called_once()
            assert response.json()["lat"] == 10
            assert response.json()["long"] == 20
            assert response.json()["owner"]["id_user"] == str(user.id_user)
            assert response.status_code == 200


def test_get_all_spot(spot_client, spot, session):
    session.add(spot)
    session.commit()
    response = spot_client.get_all()
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
def test_update_spot(spot, fastapi_dep, session, spot_client, field, expected_field):
    session.add(spot)
    session.commit()

    with fastapi_dep(app).override({get_id_user_by_auth_token: spot.id_user}):
        data = {field: expected_field}
        response = spot_client.update(id=spot.id_spot, update=json.dumps(data))
        assert response.status_code == 200
        assert response.json()[field] == expected_field


def test_delete_spot(spot, fastapi_dep, session, spot_client):
    session.add(spot)
    session.commit()

    with fastapi_dep(app).override({get_id_user_by_auth_token: spot.id_user}):
        spot_client.delete(id=spot.id_spot)
        response = spot_client.get_by_id(id=spot.id_spot)
        assert response.status_code == 404
        assert response.json()["detail"] == "Spot not found"
