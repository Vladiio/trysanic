FROM python:3.7.3-slim

WORKDIR /usr/src/trysanic

COPY . .

RUN pip install --no-cache-dir celery redis

WORKDIR ../

CMD celery -A trysanic worker -l info

