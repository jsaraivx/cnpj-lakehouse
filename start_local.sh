#!/usr/bin/env bash
set -euo pipefail

# start_local: macOS / Linux helper to create venv, install deps and start MinIO via docker-compose
# Usage: ./start_local

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "[cnpj-lakehouse] Starting local environment (macOS/Linux)..."

# create virtualenv if missing
if [ ! -d ".venv" ]; then
  echo "Creating Python virtualenv at .venv..."
  python3 -m venv .venv
fi

echo "Activating virtualenv... (run 'deactivate' to leave)"
# shellcheck disable=SC1091
source .venv/bin/activate

if [ -f "local-requirements.txt" ]; then
  echo "Installing local development requirements (PySpark + Jupyter + pytest)..."
  python -m pip install --upgrade pip
  python -m pip install -r local-requirements.txt
elif [ -f "requirements.txt" ]; then
  echo "Installing Python requirements..."
  python -m pip install --upgrade pip
  python -m pip install -r requirements.txt
else
  echo "No requirements.txt found; skipping pip install."
fi

# start MinIO via docker-compose (local-infra/docker-compose.yml)
COMPOSE_DIR="$ROOT_DIR/local-infra"
if [ -d "$COMPOSE_DIR" ]; then
  echo "Starting MinIO with Docker Compose..."
  (cd "$COMPOSE_DIR" && (docker compose up -d || docker-compose up -d))
  echo "Docker Compose started (MinIO)."
else
  echo "Warning: $COMPOSE_DIR not found. Skipping Docker Compose start."
fi

echo "Local environment ready. Virtualenv is active in this shell."
echo "To run ETL: activate venv (if not already) and run your Python/PySpark commands." 

exit 0
