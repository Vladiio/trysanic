from blog import blog
from blog import db

from app import app


async def test_index_returns_200():
    async with app.db.acquire() as conn:
        await conn.execute(db.posts.insert(), content='test')

    request, response = app.test_client.get('/')
    import pdb
    pdb.set_trace()
    assert response.status == 200


def test_index_returns_post():
    request, response = app.test_client.get('/')


def test_index_put_not_allowed():
    request, response = app.test_client.put('/')
    assert response.status == 405
