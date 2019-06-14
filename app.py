from sanic import Sanic
from sanic.response import json

from blog import blog
from core import db

app = Sanic(__name__)


def create_app():
    app = Sanic(__name__)
    app.blueprint(blog.bp)

    app.register_listener(db.setup_db, 'before_server_start')
    app.register_listener(db.create_tables, 'after_server_start')
    app.register_listener(db.close_db, 'after_server_stop')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
