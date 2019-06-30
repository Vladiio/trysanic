FROM python:3.7.3-alpine

WORKDIR /usr/src

RUN pip install --no-cache-dir celery redis requests

ENV RESULT_BACKEND_HOST='redis' \
    BROKER_HOST='rabbit'

CMD celery -A trysanic worker -l info
