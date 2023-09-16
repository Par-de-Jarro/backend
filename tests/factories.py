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
