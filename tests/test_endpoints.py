
import requests
from blog import blog


from app import app


def test_index_returns_200():
    request, response = app.test_client.get('/')
    assert response.status == 200


def test_index_returns_post():
    request, response = app.test_client.get('/')


def test_index_put_not_allowed():
    request, response = app.test_client.put('/')
    assert response.status == 405
