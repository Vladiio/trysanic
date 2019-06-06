import json

from sanic import Blueprint, response

from .db import post
from .serializers import PostSchema

bp = Blueprint('blog')


@bp.route('/')
async def posts(request):
    async with request.app.db.acquire() as conn:
        posts = await conn.execute(post.select())
        posts = await posts.fetchall()

    posts = [{key: value for key, value in row.items()} for row in posts]
    result = PostSchema().dumps(posts, many=True)

    return response.json({'posts': result})


@bp.route('/create', methods=['POST'])
async def create_post(request):
    print(request.json)
    if not request.json or 'content' not in request.json:
        return response.json({}, status=400)

    async with request.app.db.acquire() as conn:
        result = await conn.execute(
            post.insert().values(content=request.json['content']))
        inserted_id = await result.scalar()

    return response.json({'id': inserted_id}, status=201)
