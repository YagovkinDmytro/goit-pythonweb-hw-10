#!/bin/bash

echo "Waiting for PostgreSQL..."

# Проверяем готовность PostgreSQL
until pg_isready -h postgres -p 5432 -U $POSTGRES_USER; do
  echo "Waiting for database..."
  sleep 2
done

echo "Applying Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload