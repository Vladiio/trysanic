broker_url='pyamqp://guest@localhost//'
result_backend='redis://localhost'

include = ['trysanic.tasks']

task_routes = {
    'tasks.*': 'priority.high',
    'tasks.mul': 'priority.low'
}

task_annotations = {
    'tasks.add': { 'rate_limit': '1/m' }
}

