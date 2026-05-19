#!/usr/bin/env bash
set -euo pipefail

cp -n .env.example .env || true
cp -n apps/web/.env.example apps/web/.env.local || true
cp -n apps/api/.env.example apps/api/.env || true

corepack enable
pnpm install

echo "Bootstrap complete."
