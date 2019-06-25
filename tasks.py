import random

from celery.utils.log import get_task_logger
from celery import Task, chain

from .celery import app

logger = get_task_logger(__name__)

@app.task
def add(x, y):
    return x + y

@app.task
def mul(x, y):
    return x * y

@app.task
def xsum(numbers, ignore_result=True):
    return sum(numbers)


@app.task(bind=True, default_retry_delay=30*60)
def bound_add(self, a, b):
    # logger.info(self.request.id)
    logger.info(f'Adding {a} + {b}')

    if random.choice(range(2)) > 0:
        raise self.retry()
    return a + b


class DBTask(app.Task):
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = 'connection'
        return self._db

    def on_success(self, *args):
        print('success')


@app.task(base=DBTask)
def process_rows():
    print(process_rows.db)


def update_page(url):
    chained = chain(
                fetch_doc.s(url),
                parse_doc.s(),
                save_parsed_doc.s(url)
            )
    chained()


@app.task
def fetch_doc(url):
    print(f'fetching document at {url}')
    return 'document'

@app.task
def parse_doc(doc):
    print(f'parsing the doc {doc}')
    return 'body'

@app.task(ignore_result=True)
def save_parsed_doc(url, info):
    print(f'saved! (url: {url}, info: {info})')


@app.task(bind=True)
def hello(self, a, b):
    import time
    time.sleep(1)
    self.update_state(
            state='PROGRESS', meta=dict(progress=50)
    )
    time.sleep(1)
    self.update_state(
            state='PROGRESS', meta=dict(progress=90)
    )
    time.sleep(1)
    return f'hello world: {a + b}'

def on_raw_message(body):
    print(body)



