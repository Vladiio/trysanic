import pytest

from app import create_app


@pytest.yield_fixture()
def app():
    yield create_app()


@pytest.fixture
def test_cli(app, loop, sanic_client):
    return loop.run_until_complete(sanic_client(app))
