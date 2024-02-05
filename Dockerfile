# Install requirements
FROM python:3.11-slim as core

WORKDIR /app

RUN pip install poetry==1.6.1
COPY ./poetry.lock /app/poetry.lock
COPY ./pyproject.toml /app/pyproject.toml

# Only application
FROM core as slim

RUN apt update -y && apt install -y curl

RUN poetry install --only main --all-extras
COPY ./raterover /app/raterover
COPY ./.env .
