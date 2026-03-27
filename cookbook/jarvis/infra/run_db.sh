#!/usr/bin/env bash
# =============================================================================
# Jarvis — Start local database and apply schema
# =============================================================================
# Usage: ./cookbook/jarvis/infra/run_db.sh
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose.yml"
DB_URL="postgresql://ai:ai@localhost:5532/ai"

echo "Starting Jarvis database..."
docker compose -f "$COMPOSE_FILE" up -d db redis

echo "Waiting for database to be ready..."
until docker compose -f "$COMPOSE_FILE" exec -T db pg_isready -U ai -d ai > /dev/null 2>&1; do
    sleep 1
done

echo "Applying schema..."
psql "$DB_URL" -f "$REPO_ROOT/cookbook/jarvis/database/schema.sql"

echo "Loading demo seed data..."
psql "$DB_URL" -f "$REPO_ROOT/cookbook/jarvis/database/seed_demo.sql"

echo ""
echo "Database ready: $DB_URL"
echo "Redis ready:    localhost:6379"
