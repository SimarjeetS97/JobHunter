FROM node:22-alpine AS base
WORKDIR /app
RUN corepack enable

FROM base AS deps
COPY package.json pnpm-workspace.yaml ./
COPY apps/web/package.json apps/web/package.json
COPY packages ./packages
RUN pnpm install --filter @apps/web... --frozen-lockfile=false

FROM deps AS build
COPY . .
RUN pnpm --filter @apps/web build

FROM base AS runner
ENV NODE_ENV=production
COPY --from=build /app/apps/web/.next /app/apps/web/.next
COPY --from=build /app/apps/web/public /app/apps/web/public
COPY --from=build /app/apps/web/package.json /app/apps/web/package.json
COPY --from=build /app/node_modules /app/node_modules
WORKDIR /app/apps/web
EXPOSE 3000
CMD ["pnpm", "start"]
