FROM python:3.7.3-alpine

WORKDIR /usr/src

RUN pip install --no-cache-dir celery redis requests

ENV RESULT_BACKEND_HOST='redis' \
    BROKER_HOST='rabbit' \
    TELEGRAM_TOKEN='892863855:AAEzgXHnxEp3sZEiJv5uORI6k1ZdzQK-xWY'

CMD celery -A trysanic worker -l info
