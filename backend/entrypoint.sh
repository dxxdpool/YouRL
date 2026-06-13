#!/bin/sh

set -e

echo "Running migrations..."

.venv/bin/alembic upgrade head

echo "Starting application..."

exec .venv/bin/uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000