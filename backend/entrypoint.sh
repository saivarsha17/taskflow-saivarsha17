#!/bin/bash
set -e
echo "Waiting for database..."
while ! pg_isready -h "${DB_HOST:-db}" -p "${DB_PORT:-5432}" -U "${DB_USER:-postgres}"; do
  sleep 1
done
echo "Database is ready!"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Seeding database..."
python seed.py

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000
