#!/bin/bash
# release.sh - ProjectNemo production release
# Run from local dev machine. Merges dev -> main, tags, deploys to REDACTED-HOST.
# NOTE: Agent may be running on this project - check before releasing.
set -e

NODE_IP="10.0.0.103"  # REDACTED-HOST ethernet; use .107 if on WiFi
NODE_USER="kamilo"
TARGET_DIR="/home/kamilo/nemo/ProjectNemo"
INTEGRATION_BRANCH="dev"
KUMA_PUSH_URL=""  # TODO: create Push monitor in REDACTED-HOST:3001 (Kuma migrated from REDACTED-HOST), paste URL here

echo "[1/5] Merging $INTEGRATION_BRANCH -> main..."
git checkout main && git pull origin main
git merge "$INTEGRATION_BRANCH" --no-edit
VERSION="v$(date +%Y.%m.%d-%H%M)"
git tag -a "$VERSION" -m "Release $VERSION"
git push origin main --tags
git checkout "$INTEGRATION_BRANCH"
echo "Tagged $VERSION"

echo "[2/5] Connecting to $NODE_USER@$NODE_IP..."
ssh "$NODE_USER@$NODE_IP" bash << ENDSSH
set -e
cd "$TARGET_DIR"

echo "[3/5] Backing up SQLite..."
mkdir -p ./backups
if docker ps -q -f name="nemo-api" | grep -q .; then
  docker compose cp nemo-api:/app/data/nemo.db ./backups/nemo_\$(date +%Y%m%d_%H%M%S).db
  echo "SQLite backup saved."
else
  echo "WARNING: nemo-api not running, skipping backup."
fi

echo "[4/5] Pulling code..."
git fetch --tags && git checkout main && git pull origin main

echo "[5/5] Rebuilding containers..."
docker compose down && docker compose up -d --build
echo "Done. SQLAlchemy create_all runs on startup."
ENDSSH

if [ -n "$KUMA_PUSH_URL" ]; then
  curl -s "${KUMA_PUSH_URL}?status=up&msg=${VERSION}&ping=" > /dev/null
  echo "Kuma notified."
fi

echo ""
echo "ProjectNemo $VERSION deployed."
