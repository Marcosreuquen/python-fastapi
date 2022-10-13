## Python version

> 3.10.6

## pip version

> 22.2.2

## requirements

> requirements.txt

# Initialize virtual environment

`python -m venv <environment>`

# Install requirements

`pip install -r requirements.txt`

# Start server:

`uuvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`

# Build docker image

`docker-compose docker-compose-dev.yml up -d`

# View image logs

`docker-compose -f docker-compose-dev.yml --follow logs`

# Shutdown image

`docker-compose -f docker-compose-dev.yml down`

# Create migration

`alembic revision --autogenerate`

# Upgrade DB

`alembic upgrade head`
