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


@register_tables_creator
async def create_authors(conn):
    await conn.execute('DROP TABLE IF EXISTS authors')
    await conn.execute('''
        CREATE TABLE authors (
            id serial PRIMARY KEY,
            name varchar(255) UNIQUE
        )
    ''')


@register_tables_creator
async def create_posts(conn):
    await conn.execute('DROP TABLE IF EXISTS posts')
    await conn.execute('''
        CREATE TABLE posts (
            id serial PRIMARY KEY,
            content varchar(255),
            author_id integer REFERENCES authors
        )
    ''')
