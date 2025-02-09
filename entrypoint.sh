#!/bin/sh

set -e  # Exit immediately if a command exits with a non-zero status

# Wait for PostgreSQL to be ready
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\q"; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done

echo "Postgres is up - continuing..."

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Django server
echo "Starting Django server..."
exec "$@"
