broker_url='pyamqp://guest@localhost//'
result_backend='redis://localhost'

# include = ['trysanic.tasks']

task_routes = {
    'tasks.add': 'high'
}

task_annotations = {
    'tasks.add': { 'rate_limit': '1/m' }
}
