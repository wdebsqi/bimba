import pytest

from .. import create_app


@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.testing = True
    return app


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()
