from sanic.exceptions import SanicException, MethodNotSupported
import pytest

from blog import blog, db


@pytest.fixture
async def populated_author_id(test_cli):
    author = dict(name='Vlad')
    async with test_cli.app.db.acquire() as conn:
        return (await conn.scalar(db.author.insert().values(**author)))


@pytest.fixture
async def populated_posts(test_cli, populated_author_id):
    comments = [dict(content=content) for content in ['one', 'two']]
    posts = [
        dict(id=1, content='test', author='Vlad',
             comments=[]),
        dict(id=2, content='test123', author='Vlad', comments=comments)
    ]
    async with test_cli.app.db.acquire() as conn:
        post_id = None
        for post in posts:
            post_data = dict(
                content=post['content'], author_id=populated_author_id)
            post_id = await conn.scalar(db.post.insert().values(**post_data))
        for comment in comments:
            comment_id = await conn.scalar(db.comment.insert().values(**comment))
            await conn.execute(db.comments_posts.insert().values(comment_id=comment_id, post_id=post_id))

    return posts


async def test_index_returns_all_posts(test_cli, populated_posts):
    response = await test_cli.get('/')
    data = await response.json()

    assert response.status == 200
    assert 'posts' in data
    assert len(data['posts']) == len(populated_posts)


async def test_index_returns_posts_with_data(test_cli, populated_posts):
    resp = await test_cli.get('/')
    assert (await resp.json()) == dict(posts=populated_posts)


def test_index_put_not_allowed(app):
    _, resp = app.test_client.put('/')
    assert resp.status == 405
