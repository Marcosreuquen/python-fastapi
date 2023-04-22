# Requirements

## Python version

> 3.10.6

## pip version

> 22.2.2

## dependencies

> requirements.txt

# Python Environment

## Initialize virtual environment

`python -m venv <environment>`

## Install requirements

`pip install -r requirements.txt`

# Start application

## Start server:

`uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`

[Server](http://localhost:8000/)

[Docs](http://localhost:8000/docs)

## Build docker image

`docker-compose up --build -d`

## View image logs

`docker-compose logs -f api`

## Shutdown image

`docker-compose down`

# Alembic

## Create session

`alembic init alembic`

## Create migration

`alembic revision --autogenerate`

## Upgrade DB

`alembic upgrade head`
