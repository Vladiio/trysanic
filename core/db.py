import os

import sqlalchemy as sa
from aiopg.sa import create_engine

metadata = sa.MetaData()

tables_creators = []


async def create_tables(app, loop):
    async with app.db.acquire() as conn:
        for creator in tables_creators:
            await creator(conn)


def register_tables_creator(creator):
    tables_creators.append(creator)
    return creator


async def setup():
    engine = await create_engine(user='sanic',
                                 database=os.environ.get(
                                     'SANIC_APP_DB', 'trysanic'),
                                 host=os.environ.get('DB_HOST'),
                                 password='pass',
                                 echo=True)

    return engine


async def setup_db(app, loop):
    app.db = await setup()


async def close_db(app, loop):
    print('closing db...')
    app.db.close()
