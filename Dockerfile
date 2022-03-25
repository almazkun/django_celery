FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/code

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && pipenv install --system
