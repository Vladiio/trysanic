import os

from celery.schedules import crontab
from kombu import Queue
from kombu.common import Broadcast

BROKER_HOST = os.environ.get("BROKER_HOST")
RESULT_BACKEND_HOST = os.environ.get("RESULT_BACKEND_HOST")

timezone = 'Europe/Kiev'

broker_url=f'pyamqp://guest@{BROKER_HOST}//'
result_backend=f'redis://{RESULT_BACKEND_HOST}/'

imports = ['trysanic.tasks']

task_default_queue = 'default'
tasks_queues = (
        Queue('default', routing_key='task.#'),
        Queue('feed_tasks', routing_key='feed.#'),
        Broadcast('broadcast_tasks')
)
task_default_exchange = 'tasks'
task_default_exchange_type = 'topic'
task_default_routing_key = 'task.default'


task_routes = {
        'trysanic.tasks.add': { 'queue': 'high', 'routing_key': 'feed.import'}
}

task_annotations = {
    'tasks.add': { 'rate_limit': '1/m' }
}

beat_schedule = {
    'good_morning': {
        'task': 'trysanic.tasks.say_good_morning', 'schedule': crontab(hour=7, minute=30)
    }
}

