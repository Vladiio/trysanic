FROM python:3.7.3-slim

WORKDIR /usr/src/trysanic

COPY requirements.txt .

RUN apt-get update && apt-get install curl build-essential -y

RUN pip install -r requirements.txt

HEALTHCHECK --interval=10s --timeout=3s \
    CMD curl -f http://localhost:8000 || exit 1

CMD gunicorn --worker-class sanic.worker.GunicornWorker -w 4 -b :8000 app:app
