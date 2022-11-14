import pytest

from ...db.DBConnector import DBConnector
from ...db.DBLogger import DBLogger
from .. import create_app
from ..src.RequestLogger import RequestLogger


@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.testing = True
    return app


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()


@pytest.fixture(scope="module")
def db_connector():
    return DBConnector()


@pytest.fixture(scope="module")
def db_logger(db_connector):
    return DBLogger(db_connector)


@pytest.fixture(scope="module")
def request_logger(db_connector, db_logger):
    return RequestLogger(db_connector, db_logger)
