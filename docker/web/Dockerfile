FROM python:3.7.3-slim

WORKDIR /usr/src/trysanic

COPY requirements.txt .

RUN apt-get update && apt-get install build-essential -y

RUN pip install -r requirements.txt

CMD python app.py
