import uuid
from typing import Optional

import pytest

import app.common.models as models


@pytest.fixture
def make_user(session, make_university):
    defaults = dict(
        name="Ricardinho",
        email="teste@email.com",
        cellphone="11999999999",
        document_id="12345678901",
        birthdate="1990-04-13",
        course="Ciência da Computação",
        bio="Teste",
        password_hash="123456",
    )

    def _make_user(id_university: Optional[uuid.UUID] = None, **overrides):
        new_defaults = defaults
        if not id_university:
            university = make_university()
            session.add(university)
            session.commit()

            new_defaults = dict(id_university=university.id_university, **new_defaults)
        return models.User(id_user=uuid.uuid4(), **{**new_defaults, **overrides})

    return _make_user


@pytest.fixture
def make_university():
    defaults = dict(
        name="Universidade Federal de Campina Grande",
        slug="UFCG",
        lat=-7.216306580255391,
        long=-35.909625553967125,
    )

    def _make_university(**overrides):
        return models.University(id_university=uuid.uuid4(), **{**defaults, **overrides})

    return _make_university


@pytest.fixture
def make_spot():
    defaults = dict(
        name="Spot Teste",
        description="Teste",
        lat=-7.216306580255391,
        long=-35.909625553967125,
        personal_quota=10,
        type="house",
        value=200,
        street="Avenida de Testes",
        zip_code="58434500",
        number="5255",
        complement="B20",
        city="Campina Grande",
        state="PB",
        key="convenience: {rooms_quantity: 2, bathrooms_quantity: 2, has_elevator: true},"
        + "allowance: {allow_pet: true, allow_smoker: true}",
    )

    def _make_spot(**overrides):
        new_defaults = defaults
        user = make_user()
        new_defaults = dict(id_user=user.id_user, **new_defaults)
        return models.Spot(id_spot=uuid.uuid4(), **{**new_defaults, **overrides})

    return _make_spot
