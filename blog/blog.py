import json
from collections import defaultdict

from sanic import Blueprint, response
from sanic.exceptions import NotFound
import sqlalchemy as sa
import aiohttp

from . import db
from .serializers import PostSchema, CommentSchema

bp = Blueprint('blog')


@bp.route('/')
async def posts(request):
    posts = []
    comments_by_post_id = defaultdict(list)

    async with request.app.db.acquire() as conn:
        join = sa.join(db.post, db.author)
        stmt = sa.select([db.post.c.id, db.post.c.content,
                          db.author.c.name.label('author')]).select_from(join)
        async for post in await conn.execute(stmt):
            posts.append({column: value for column, value in post.items()})

        post_ids = [post['id'] for post in posts]
        join = db.comment.join(db.comments_posts)

        comments = await conn.execute(
            sa.select(
                [db.comment.c.id, db.comment.c.content, db.comments_posts.c.post_id]
            ).select_from(join).where(db.comments_posts.c.post_id.in_(post_ids))
        )

        async for comment in comments:
            serialized_comment = {
                column: value for column, value in comment.items()}
            comments_by_post_id[comment.post_id].append(serialized_comment)

    for post in posts:
        post.setdefault('comments', [])
        comments = comments_by_post_id.get(post['id'])
        comments and post['comments'].append(comments)

    return response.json(dict(posts=posts))


@bp.route('/', methods=['POST'])
async def create_post(request):
    post_data, errors = PostSchema().load(request.json)
    author_data = post_data.pop('author', None)

    if post_data is None or errors:
        return response.json(errors, status=400)

    async with request.app.db.acquire() as conn:
        async with conn.begin() as trans:
            author_id = await conn.scalar(
                db.author.insert().values(**author_data)
            )
            post_id = await conn.scalar(
                db.post.insert().values(author_id=author_id, **post_data)
            )
    return response.json({'id': post_id}, status=201)


@bp.route('/<post_id:int>')
async def post_detail(request, post_id):
    async with request.app.db.acquire() as conn:
        post_proxy = await fetch_entity_by_id(conn, db.post, post_id)

    post, _ = PostSchema().dump(post_proxy)
    return response.json({'post': post})


@bp.route('/<post_id:int>', methods=['DELETE'])
async def post_delete(request, post_id):
    async with request.app.db.acquire() as conn:
        await conn.execute(
            db.post.delete().where(db.post.c.id == post_id))

    return response.json({}, status=204)


@bp.route('/<post_id:int>', methods=['PATCH'])
async def post_update(request, post_id):
    post_data, errors = PostSchema().load(request.json)
    if post_data is None or errors:
        return response.json(errors, status=400)

    async with request.app.db.acquire() as conn:
        query = db.post.update().where(db.post.c.id == post_id).values(
            **post_data)
        await conn.execute(query)

    return response.json({})


@bp.route('/<post_id:int>/comments/')
async def comments_list(request, post_id):
    async with request.app.db.acquire() as conn:
        join = sa.join(db.comment, db.comments_posts)
        comment = await conn.execute(db.comment.select().select_from(join).where(
            db.comments_posts.c.post_id == post_id))

        comments = [{column: value for column, value in row.items()}
                    for row in comment]
    return response.json(dict(comments=comments))


@bp.route('/<post_id:int>/comments/', methods=['POST'])
async def create_comment(request, post_id):
    async with request.app.db.acquire() as conn:
        query = sa.select([db.post.c.id]).where(db.post.c.id == post_id)
        fetched_post_id = await conn.scalar(query)
        if not fetched_post_id:
            return response.json({}, status=404)

        comment_data, errors = CommentSchema().load(request.json)
        if comment_data is None or errors:
            return response.json(dict(errors=errors), status=400)

        async with conn.begin() as trans:
            comment_id = await conn.scalar(db.comment.insert().values(**comment_data))
            await conn.execute(
                db.comments_posts.insert().values(comment_id=comment_id, post_id=fetched_post_id)
            )
    return response.json(dict(id=comment_id))


@bp.route('/github')
async def github_profile_into(request):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.github.com/users/vladiio') as resp:
            return response.raw(await resp.read(), content_type='application/json')


async def fetch_entity_by_id(conn, entity, id):
    result_proxy = await conn.execute(entity.select().where(entity.c.id == id))
    row_proxy = await result_proxy.fetchone()
    if row_proxy is None:
        raise NotFound('Not found')
    return row_proxy
