import uuid

import pytest

import app.common.models as models


@pytest.fixture
def make_todo():
    defaults = dict(description="UMA DESCRIÇÃO MAROTA")

    def make_todo(**overrides):
        return models.Todo(id_todo=uuid.uuid4(), **{**defaults, **overrides})

    return make_todo
