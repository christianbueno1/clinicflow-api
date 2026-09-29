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

# echo "==> Removing PostgreSQL container..."
# podman rm -f "$DB_BOX_NAME" 2>/dev/null || true

echo "==> Removing PostgreSQL pod..."
podman pod rm -f "$DB_POD_NAME" 2>/dev/null || true

echo "==> Removing network..."
podman network rm "$NETWORK_NAME" 2>/dev/null || true

echo
echo "PostgreSQL container, pod and network removed."
echo "Volume preserved: $DB_VOL_NAME"
echo
echo "To remove the database data permanently:"
echo "  podman volume rm $DB_VOL_NAME"