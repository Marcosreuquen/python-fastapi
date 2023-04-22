#!/bin/bash
echo "Consuming environment variables..."
set -a
. ./.env
set +a
echo "Generating Database revision..."
alembic revision --autogenerate
echo "Revision done."
echo "Making migration..."
alembic upgrade head
echo "Migration done."