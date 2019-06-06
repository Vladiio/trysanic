import json

from sanic import Blueprint, response

from .db import post
from .serializers import PostSchema

bp = Blueprint('blog')


@bp.route('/')
async def posts(request):
    async with request.app.db.acquire() as conn:
        posts = await conn.execute(post.select())
        posts, errors = PostSchema().dump(posts, many=True)
        return response.json({'posts': posts})


@bp.route('/create', methods=['POST'])
async def create_post(request):
    post_data, errors = PostSchema().load(request.json)
    if errors:
        return response.json(errors, status=400)

    async with request.app.db.acquire() as conn:
        result = await conn.execute(
            post.insert().values(**post_data))
        inserted_id = await result.scalar()
    return response.json({'id': inserted_id}, status=201)
