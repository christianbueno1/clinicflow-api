#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env.db"

if [[ ! -f "$ENV_FILE" ]]; then
    echo "Error: $ENV_FILE not found."
    echo "Create it from .env.db.example:"
    echo "  cp .env.db.example .env.db"
    exit 1
fi

set -a
source "$ENV_FILE"
set +a

echo "==> Creating network..."
podman network create "$NETWORK_NAME" 2>/dev/null || true

echo "==> Creating volume..."
podman volume create "$DB_VOL_NAME" 2>/dev/null || true

echo "==> Creating pod..."
podman pod create \
    --name "$DB_POD_NAME" \
    -p "${DB_PORT}:5432" \
    --network "$NETWORK_NAME" \
    2>/dev/null || true

echo "==> Creating PostgreSQL container..."
podman run -d \
    --name "$DB_BOX_NAME" \
    --pod "$DB_POD_NAME" \
    --restart=always \
    -e POSTGRES_USER="$POSTGRES_USER" \
    -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
    -e POSTGRES_DB="$POSTGRES_DB" \
    -v "${DB_VOL_NAME}:/var/lib/postgresql" \
    "$DB_IMAGE"

echo
echo "PostgreSQL container created:"
echo "  Pod:       $DB_POD_NAME"
echo "  Container: $DB_BOX_NAME"
echo "  Database:  $POSTGRES_DB"
echo "  User:      $POSTGRES_USER"
echo "  Port:      $DB_PORT"