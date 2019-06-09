import sqlalchemy as sa

from core.db import metadata, register_tables_creator

post = sa.Table(
    'posts',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('content', sa.String(255)),
    sa.Column('author_id', sa.ForeignKey('authors.id')),
)

author = sa.Table(
    'authors',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(255), unique=True),
)

comment = sa.Table(
    'comments', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('content', sa.String, nullable=False)
)

comments_posts = sa.Table(
    'comments_posts', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('comment_id', sa.ForeignKey('comments.id'), primary_key=True),
    sa.Column('post_id', sa.ForeignKey('posts.id'), primary_key=True)
)


@register_tables_creator
async def create_authors(conn):
    await conn.execute('DROP TABLE IF EXISTS authors CASCADE')
    await conn.execute('''
        CREATE TABLE authors (
            id serial PRIMARY KEY,
            name varchar(255) UNIQUE
        )
    ''')


@register_tables_creator
async def create_posts(conn):
    await conn.execute('DROP TABLE IF EXISTS posts CASCADE')
    await conn.execute('''
        CREATE TABLE posts (
            id serial PRIMARY KEY, 
            content varchar(255),
            author_id integer REFERENCES authors
        )
    ''')


@register_tables_creator
async def create_comment(conn):
    await conn.execute('DROP TABLE IF EXISTS comments CASCADE')
    await conn.execute('''
        CREATE TABLE comments(
            id SERIAL PRIMARY KEY,
            content text NOT NULL
        )
    ''')


@register_tables_creator
async def create_comments_posts(conn):
    await conn.execute('DROP TABLE IF EXISTS comments_posts')
    await conn.execute('''
        CREATE TABLE comments_posts (
            id SERIAL PRIMARY KEY,
            post_id integer REFERENCES posts,
            comment_id integer REFERENCES comments
        )
    ''')
