import json
from unittest.mock import Mock
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_id_user_by_auth_token
from app.main import app
from app.spot.schemas.spot import SpotCreate, SpotView

from .base_client import BaseClient

client = TestClient(app)


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
    mock_service = Mock()
    mock_service.create.return_value = SpotView(
        id=UUID("01234567-89ab-cdef-0123-456789abcdef"), name="Test Spot"
    )
    session.add(spot)
    session.commit()

    with fastapi_dep(app).override({get_id_user_by_auth_token: user.id_user}):
        response = client.post(
            "/spot/",
            json={"name": "Test Spot", "description": "Test Description"},
            headers={"Authorization": "Bearer mocktoken"},
        )

    assert response.status_code == 200
    assert response.json() == {"id": "01234567-89ab-cdef-0123-456789abcdef", "name": "Test Spot"}
    mock_service.create.assert_called_once_with(
        create=SpotCreate(name="Test Spot", description="Test Description")
    )


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
