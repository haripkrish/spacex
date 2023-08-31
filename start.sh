#! /usr/bin/env bash

# Run migrations
echo "Running Alembic migrations..."
sleep 5
alembic upgrade head

echo "Running the Data Pipeline..."
exec python main.py