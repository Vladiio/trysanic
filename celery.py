from celery import Celery


app = Celery('trysanic')
app.config_from_object('trysanic.celeryconfig')


if __name__ == '__main__':
    app.start()
