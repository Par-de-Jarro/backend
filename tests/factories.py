import pytest

from app.user.schemas.user import UserCreate


@pytest.fixture
def make_todo():
    ...


@pytest.fixture
def make_user():
    user = UserCreate()
    user.name = "Ricardinho"
    user.email = "teste@email.com"
    user.cellphone = "11999999999"
    user.document_id = "12345678901"
    user.birthdate = "1990-04-13"
    user.course = "Ciência da Computação"
    user.bio = "Teste"
    return user
