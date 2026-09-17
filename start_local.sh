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
  COMPOSE_ENV_ARGS=()
  if [ -f "$ROOT_DIR/.env" ]; then
    COMPOSE_ENV_ARGS=(--env-file "$ROOT_DIR/.env")
  fi
  (cd "$COMPOSE_DIR" && (docker compose "${COMPOSE_ENV_ARGS[@]}" up -d || docker-compose "${COMPOSE_ENV_ARGS[@]}" up -d))
  echo "Docker Compose started (MinIO)."
else
  echo "Warning: $COMPOSE_DIR not found. Skipping Docker Compose start."
fi

echo "Local environment ready. Virtualenv is active in this shell."
echo "MinIO Console: http://localhost:9001"
echo "MinIO API: http://localhost:9000"
echo "Credentials: minioadmin / minioadmin"
echo "Buckets: cnpj-raw, cnpj-bronze, cnpj-silver, cnpj-gold, cnpj-checkpoints"
echo "Spark UI: http://localhost:4040"
echo "Use: python -m src.jobs.local_spark_runtime"

# Preserve activation when sourced, while still supporting direct execution.
return 0 2>/dev/null || exit 0
