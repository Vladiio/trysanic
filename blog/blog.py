import json

from sanic import Blueprint, response
from sanic.exceptions import NotFound
import sqlalchemy as sa

from . import db
from .serializers import PostSchema

bp = Blueprint('blog')


@bp.route('/')
async def posts(request):
    async with request.app.db.acquire() as conn:
        posts = await conn.execute(
            sa.select([db.post, db.author.c.name.label('author_name')]).select_from(
                db.post.outerjoin(db.author))
        )
        posts = [
            {column: value for column, value in post.items()} async for post in posts
        ]
        return response.json({'posts': posts})


@bp.route('/', methods=['POST'])
async def create_post(request):
    post_data, errors = PostSchema().load(request.json)
    author_data = post_data.pop('author', None)

    if post_data is None or errors:
        return response.json(errors, status=400)

    async with request.app.db.acquire() as conn:
        author_result = await conn.execute(
            db.author.insert().values(**author_data)
        )
        author_id = await author_result.scalar()

        post_result = await conn.execute(
            db.post.insert().values(author_id=author_id, **post_data)
        )
        inserted_id = await post_result.scalar()
    return response.json({'id': inserted_id}, status=201)


@bp.route('/<post_id:int>')
async def post_detail(request, post_id):
    async with request.app.db.acquire() as conn:
        post_proxy = await fetch_entity_by_id(conn, db.post, post_id)

    post, _ = PostSchema().dump(post_proxy)
    return response.json({'post': post})


@bp.route('/<post_id:int>', methods=['DELETE'])
async def post_delete(request, post_id):
    async with request.app.db.acquire() as conn:
        result = await conn.execute(
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


async def fetch_entity_by_id(conn, entity, id):
    result_proxy = await conn.execute(entity.select().where(entity.c.id == id))
    row_proxy = await result_proxy.fetchone()
    if row_proxy is None:
        raise NotFound('Not found')
    return row_proxy
