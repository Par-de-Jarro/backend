import pytest

from app.user.schemas.user import UserCreate


@pytest.fixture
def make_todo():
    ...


@pytest.fixture
def make_user():
    user = UserCreate(
        name="Ricardinho",
        email="teste@email.com",
        cellphone="11999999999",
        document_id="12345678901",
        birthdate="1990-04-13",
        course="Ciência da Computação",
        bio="Teste",
        password="123456",
    )
    return user
