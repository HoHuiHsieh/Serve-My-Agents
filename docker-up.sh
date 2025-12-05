#!/usr/bin/env bash
set -e

# Usage: ./docker-up.sh [dev|prod] [--detach]
# Default profile: dev

PROFILE="${1:-dev}"
DETACH_FLAG="${2:-}"

# Normalize detach flag: accept --detach or -d
if [ "$DETACH_FLAG" = "--detach" ]; then
  DETACH="-d"
else
  DETACH="$DETACH_FLAG"
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker not found. Please install and start Docker Desktop or Docker Engine."
  exit 1
fi

# Prefer modern 'docker compose' CLI
if docker compose version >/dev/null 2>&1; then
  DOCKER_COMPOSE_CMD="docker compose"
elif docker-compose version >/dev/null 2>&1; then
  DOCKER_COMPOSE_CMD="docker-compose"
else
  echo "docker compose plugin or docker-compose not found."
  exit 1
fi

# Detect whether the chosen compose command supports --profile by checking help output
if $DOCKER_COMPOSE_CMD up --help 2>/dev/null | grep -q -- '--profile'; then
  SUPPORTS_PROFILE=true
else
  SUPPORTS_PROFILE=false
fi

# Map profile -> services when --profile is not available
if [ "$SUPPORTS_PROFILE" = true ]; then
  echo "Using profile: $PROFILE (compose supports --profile)"
  echo "Running: $DOCKER_COMPOSE_CMD up --profile $PROFILE --build ${DETACH:-}"
  # Pull/build then bring up with profile
  $DOCKER_COMPOSE_CMD pull || true
  $DOCKER_COMPOSE_CMD up --profile "$PROFILE" --build ${DETACH:-}
else
  # Fallback to service names
  case "$PROFILE" in
    dev) SERVICES="api-dev" ;;
    prod) SERVICES="api" ;;
    *) SERVICES="$PROFILE" ;; # allow specifying a custom service name
  esac

  echo "Using profile fallback -> services: $SERVICES (compose does NOT support --profile)"
  echo "Running: $DOCKER_COMPOSE_CMD up --build ${DETACH:-} $SERVICES"
  # Pull/build then bring up specific services
  $DOCKER_COMPOSE_CMD pull $SERVICES || true
  $DOCKER_COMPOSE_CMD up --build ${DETACH:-} $SERVICES
fi
