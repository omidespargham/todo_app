FROM python:3.8-slim-buster

WORKDIR /myproject

ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1 

RUN apt-get update && apt-get install -y build-essential libpq-dev

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt && \ 
    pip install gunicorn psycopg2;
