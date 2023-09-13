import uuid

import pytest

import app.common.models as models


@pytest.fixture
def make_user():
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

    def make_user(**overrides):
        return models.User(id_user=uuid.uuid4(), **{**defaults, **overrides})

    return make_user
