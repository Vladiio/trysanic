import sqlalchemy as sa

from core.db import metadata, register_tables_creator


@register_tables_creator
async def create_tables(conn):
    await conn.execute('DROP TABLE IF EXISTS posts')
    await conn.execute('''
        CREATE TABLE posts (
            id serial PRIMARY KEY,
            content varchar(255)
        )
    ''')


post = sa.Table(
    'posts',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('content', sa.String(255)),
)
