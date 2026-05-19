# AI Engineering Rules

## General Rules
- Always think step-by-step
- Never hallucinate libraries
- Never invent APIs
- Prefer maintainable code over clever code
- Keep files under 400 lines
- Use modular architecture

## Backend Rules
- Use FastAPI
- Use async everywhere possible
- Use SQLAlchemy ORM
- Use Pydantic DTOs
- Use repository-service pattern
- Use dependency injection

## Frontend Rules
- Use Next.js App Router
- Use TypeScript strict mode
- Use Tailwind + shadcn/ui
- Use TanStack Query
- Use Zustand only when needed

## AI Rules
- Use OpenAI Responses API
- Use structured outputs
- Never parse raw text when JSON schema can be used
- Add retry handling
- Add rate limiting

## Database Rules
- PostgreSQL
- Use migrations
- Normalize schema properly
- Use pgvector for embeddings

## Security Rules
- Validate all inputs
- Never expose secrets
- Use environment variables
- Sanitize file uploads

## Testing Rules
- Write tests for all services
- Use pytest
- Use Playwright for e2e tests

## Review Rules
Before finalizing any feature:
1. check scalability
2. check security
3. check maintainability
4. check type safety
5. check edge cases
