from kombu import Queue


broker_url='pyamqp://guest@localhost//'
result_backend='redis://localhost'

task_default_queue = 'default'
tasks_queues = (
        Queue('default', routing_key='task.#'),
        Queue('feed_tasks', routing_key='feed.#'),
)
task_default_exchange = 'tasks'
task_default_exchange_type = 'topic'
task_default_routing_key = 'task.default'

imports = ['trysanic.tasks']

task_routes = {
        'trysanic.tasks.add': { 'queue': 'high', 'routing_key': 'feed.import'}
}

task_annotations = {
    'tasks.add': { 'rate_limit': '1/m' }
}

beat_schedule = {
    'test': {'task': 'trysanic.tasks.add', 'schedule': 10.0, 'args': (4, 4)}
}
