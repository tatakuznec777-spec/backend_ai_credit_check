#!/bin/bash
set -e

echo "Applying database migrations..."
python -m alembic upgrade head

echo "Starting application..."
exec "$@"
