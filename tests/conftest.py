import os

import pytest
import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from sqlalchemy_utils import create_database, database_exists

from app.api.deps import get_db, hass_access, token_auth
from app.core.settings import SQLALCHEMY_DATABASE_URL
from app.main import app
from tests.factories import make_spot, make_university, make_user  # noqa: F401

engine = create_engine(SQLALCHEMY_DATABASE_URL)


@pytest.fixture()
def session():
    if not engine.url.database.endswith("_test"):
        raise Exception("Dear lord! for your safety only db name ending `_test` is allowed.")

    if not database_exists(engine.url):
        create_database(engine.url)

    root_dir = os.getcwd()
    script_location = root_dir + "/migrations"
    alembic_ini = root_dir + "/alembic.ini"
    config = Config(file_=alembic_ini)

    config.set_main_option("script_location", script_location)
    config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)

    # drop everything
    # command.downgrade(config, "base")
    # run migrations
    command.upgrade(config, "head")

    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    session.begin()

    # Begin a nested transaction (using SAVEPOINT).
    nested = connection.begin_nested()

    # If the application code calls session.commit, it will end the nested
    # transaction. Need to start a new one when that happens.
    @sa.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    # Rollback the overall transaction, restoring the state before the test ran.
    session.close()
    transaction.rollback()
    connection.close()


# A fixture for the fastapi test client which depends on the
# previous session fixture. Instead of creating a new session in the
# dependency override as before, it uses the one provided by the
# session fixture.
@pytest.fixture()
def client(session):
    def override_get_db():
        yield session

    def skip_auth():
        pass

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[hass_access] = skip_auth
    app.dependency_overrides[token_auth] = skip_auth
    test_client = TestClient(app)

    yield test_client
    del app.dependency_overrides[get_db]
    del app.dependency_overrides[hass_access]
    del app.dependency_overrides[token_auth]
