FROM python:3.7.3-slim

WORKDIR /usr/src/trysanic

COPY requirements.txt .

RUN apt-get update && apt-get install build-essential -y

RUN pip install -r requirements.txt

HEALTHCHECK --interval=10s --timeout=3s \
    CMD curl -f http://locahost:8000 || exit 1

CMD python app.py
