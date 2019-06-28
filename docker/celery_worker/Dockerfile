FROM python:3.7.3-alpine

WORKDIR /usr/src

RUN pip install --no-cache-dir celery redis

CMD celery -A trysanic worker -l info

