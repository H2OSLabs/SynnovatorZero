#!/bin/bash
set -euo pipefail

# Deploy script for SynnovatorZero
# Usage:
#   ./deploy.sh          - Interactive deployment
#   ./deploy.sh --ci     - Non-interactive CI mode (no prompts, strict error handling)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
CI_MODE=false
HEALTH_URL="http://localhost:9080/health"
COMPOSE_PROJECT_NAME="synnovator-zero"

# Parse arguments
for arg in "$@"; do
  case $arg in
    --ci) CI_MODE=true ;;
    *) echo "Unknown argument: $arg"; exit 1 ;;
  esac
done

log() { echo "[$(date '+%H:%M:%S')] $*"; }
err() { echo "[$(date '+%H:%M:%S')] ERROR: $*" >&2; }

# --- .env check ---
if [ ! -f "$PROJECT_DIR/.env" ]; then
  if [ -f "$PROJECT_DIR/.env.example" ]; then
    log "Creating .env from .env.example..."
    cp "$PROJECT_DIR/.env.example" "$PROJECT_DIR/.env"
  elif [ "$CI_MODE" = true ]; then
    err ".env file not found and no .env.example available."
    exit 1
  else
    err ".env.example not found. Please create .env manually."
    exit 1
  fi
fi

# --- Tag current images for rollback ---
tag_for_rollback() {
  log "Tagging current images for rollback..."
  for svc in frontend backend; do
    img="${COMPOSE_PROJECT_NAME}-${svc}:latest"
    if docker image inspect "$img" > /dev/null 2>&1; then
      docker tag "$img" "$img-prev" || true
    fi
  done
}

# --- Build & Deploy ---
deploy() {
  log "Building and starting services..."
  cd "$SCRIPT_DIR"
  docker compose build
  docker compose up -d --force-recreate
  log "Containers started, waiting for stabilization..."
  sleep 15
}

# --- Health Check ---
health_check() {
  local max_retries=12
  local interval=5

  log "Running health check at $HEALTH_URL..."
  for i in $(seq 1 $max_retries); do
    if curl -sf --max-time 5 "$HEALTH_URL" > /dev/null 2>&1; then
      log "Health check passed (attempt $i/$max_retries)"
      return 0
    fi
    log "Attempt $i/$max_retries failed, retrying in ${interval}s..."
    sleep $interval
  done

  err "Health check failed after $max_retries attempts"
  return 1
}

# --- Rollback ---
rollback() {
  log "Rolling back to previous images..."
  cd "$SCRIPT_DIR"

  for svc in frontend backend; do
    img="${COMPOSE_PROJECT_NAME}-${svc}:latest"
    prev="$img-prev"
    if docker image inspect "$prev" > /dev/null 2>&1; then
      docker tag "$prev" "$img" || true
      log "Restored $prev -> $img"
    fi
  done

  docker compose up -d --force-recreate
  sleep 15

  if curl -sf --max-time 5 "$HEALTH_URL" > /dev/null 2>&1; then
    log "Rollback successful"
  else
    err "Rollback also failed - manual intervention required"
    return 1
  fi
}

# --- Cleanup ---
cleanup() {
  log "Cleaning up old images..."
  for svc in frontend backend; do
    docker rmi "${COMPOSE_PROJECT_NAME}-${svc}:latest-prev" 2>/dev/null || true
  done
  docker image prune -f --filter "until=24h" 2>/dev/null || true
}

# --- Main ---
main() {
  log "=== SynnovatorZero Deploy ==="
  log "Mode: $([ "$CI_MODE" = true ] && echo 'CI' || echo 'Interactive')"

  tag_for_rollback
  deploy

  if health_check; then
    log "Deployment successful!"
    cleanup
  else
    err "Deployment failed!"
    if [ "$CI_MODE" = true ]; then
      rollback
      exit 1
    else
      echo ""
      read -p "Rollback to previous version? [y/N] " -n 1 -r
      echo ""
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        rollback
      fi
      exit 1
    fi
  fi

  log "=== Deploy Complete ==="
  cd "$SCRIPT_DIR"
  docker compose ps
}

main
