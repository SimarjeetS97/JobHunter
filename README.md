# AI Job Hunter Monorepo

Production-ready monorepo scaffold for an AI Job Hunter platform.

## Stack
- Next.js (App Router, TypeScript strict, Tailwind)
- FastAPI (async, SQLAlchemy, Pydantic settings)
- PostgreSQL + pgvector
- Redis
- Docker + Docker Compose
- pnpm workspaces

## Monorepo Structure
```txt
apps/
  web/              # Next.js frontend
  api/              # FastAPI backend
packages/
  types/            # Shared TypeScript contracts
  api-client/       # Shared typed API client
  config-eslint/    # Shared lint config
  config-prettier/  # Shared prettier config
infra/
  docker/           # Docker compose setup
scripts/            # Bootstrap and development scripts
.github/workflows/  # CI workflow
```

## Quick Start
1. Run bootstrap:
   ```bash
   ./scripts/bootstrap.sh
   ```
2. Start local development:
   ```bash
   ./scripts/dev.sh
   ```
3. Start full Docker stack:
   ```bash
   pnpm docker:up
   ```

## Environment
Copy these templates:
- `.env.example` -> `.env`
- `apps/web/.env.example` -> `apps/web/.env.local`
- `apps/api/.env.example` -> `apps/api/.env`

## Scripts
- `pnpm dev` - start all workspaces in dev mode
- `pnpm build` - build all workspaces
- `pnpm lint` - lint all workspaces
- `pnpm typecheck` - typecheck all workspaces
- `pnpm ci` - CI gate (lint + typecheck + build)
- `pnpm docker:up` / `pnpm docker:down` - manage compose stack

## Notes
- This scaffold intentionally excludes business logic.
- Backend is organized for repository-service pattern and dependency injection.
- API contracts are designed to be shared via workspace packages.
