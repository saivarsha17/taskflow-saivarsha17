#!/bin/bash
# Migration and seeding script
# This script runs database migrations and seeds test data

set -e

echo "================================================"
echo "TaskFlow Database Setup"
echo "================================================"

# Load environment variables
if [ -f .env ]; then
    set -a
    source .env
    set +a
else
    echo "Error: .env file not found"
    echo "Please copy .env.example to .env first"
    exit 1
fi

echo ""
echo "📊 Running migrations..."
python manage.py migrate --noinput

echo ""
echo "🌱 Seeding database with test data..."
python seed.py

echo ""
echo "✅ Database setup complete!"
echo ""
echo "Test credentials:"
echo "  Email:    test@example.com"
echo "  Password: password123"
echo ""
echo "Start the server with: python manage.py runserver"
