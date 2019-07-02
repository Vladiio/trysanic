## Jarvis - your personal butler


### Run the app locally

```bash
$ docker-compose -d up --build
$ curl http://locahost:8000
```

### Included services
* nginx
* web (sanic app)
* db (postgresql)
* celery beat
* celery worker1 (consumes from the default queue)
* celery worker2 (consumes from both high and default queues)
* rabbit (as a broker)
* redis (as a result backend)


### Environment variables

```
TELEGRAM_TOKEN - telegram bot api token
DB_PWD
DB_HOST
SANIC_APP_DB=trysanic
```

### TODO

* Deploy the app
* Sort out the issue with multiple swarm nodes
* Implement weather notification
* Implement planned activities notification
* Add CI/CD
