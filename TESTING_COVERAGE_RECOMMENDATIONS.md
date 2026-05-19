# Coverage Recommendations

## Backend (pytest + async)
- Set minimum line coverage to **85%** and branch coverage to **75%** for service and API layers.
- Gate critical modules (auth, candidate creation, file upload validation) at **90%+** line coverage.
- Use `pytest --cov=app --cov-branch --cov-report=term-missing --cov-report=xml` in CI.
- Add mutation-resistant checks for validation rules:
  - required/optional field combinations
  - boundary values (`0`, max lengths, empty strings)
  - malformed payloads and wrong content types
- Add failure-path coverage for:
  - repository exceptions
  - downstream timeouts/retries
  - idempotency and duplicate constraints

## Frontend (RTL + Playwright)
- Enforce **80%** line coverage for UI logic-heavy components and hooks.
- Prioritize user-critical journeys in Playwright:
  - submit success
  - validation rejection
  - API error toast/alert
  - retry behavior after recoverable failure
- Use MSW for deterministic API responses in component tests.
- Track untested states by mapping each server state to UI state:
  - loading
  - empty
  - success
  - recoverable error
  - fatal error

## Quality Gates
- Fail CI if:
  - backend coverage drops below threshold
  - frontend coverage drops below threshold
  - Playwright critical flow tests fail
- Publish coverage artifacts (XML + HTML) for trend monitoring.
