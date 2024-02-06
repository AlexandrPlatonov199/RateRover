# RateRover Backend

## Requirements

### Requirements: Docker

For running or testing all services you can use `Docker`. You can see instructions for installation
[here](https://docs.docker.com/engine/install/).

### Requirements: Python

For running or testing all services you can use `Python` environment. You can install Python on
your local machine directly (see [here](https://www.python.org/downloads/)) or use any wrappers
(`venv`, `pyenv`, `pipenv`, etc.).

**Python version: `3.11` or higher**

After installation Python you need install `poetry` (v1.6.1):
```shell
pip install poetry==1.6.1
```
And install all Python requirements:
```shell
poetry install --all-extras
```

## Run

### Run: Docker

Copy `.env.example` to `.env`
```shell
cp .env.example .env
```
Go to the website https://www.exchangerate-api.com/, 
create a free key, and specify it in the .env file as API_KEY_EXCHANGE=

For running

```shell
docker build .
```

```shell
docker compose build
```

```shell
docker compose up 
```

Make requests

http://localhost:7777/docs#/Course/get_course_api_v1_course__get


### Run: Python

For running separate services, please, see documentation:
1. [Currency_course](reterover/currency_course/README.md)


### Test

<p align="center">
  <img src="static\skrin.png" align="center"/>
</p>