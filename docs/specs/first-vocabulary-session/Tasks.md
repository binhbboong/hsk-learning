# Tasks: Phiên học từ vựng đầu tiên

Plan: docs/specs/first-vocabulary-session/ImplementationPlan.md

## Task-1 — Scaffold FastAPI lesson contract and fallback

- [x] Status: Complete
- Depends on: none
- Goal: Create the backend project, validated lesson/card models, controlled five-card HSK 1
  content, health endpoint and recommended-lesson endpoint using fallback content.
- Files touched: `backend/pyproject.toml`, `backend/requirements.txt`, `backend/app.py`,
  `backend/hsk_api/main.py`, `backend/hsk_api/models/lesson.py`,
  `backend/hsk_api/content/default_lesson.py`, backend routers/services and backend tests.
- Definition of done: Backend tests pass and cover FR-3, FR-4, FR-15, FR-17 and FR-18 for
  the fallback HTTP contract.
- Implemented files: `backend/app.py`, `backend/hsk_api/main.py`,
  `backend/hsk_api/models/lesson.py`, `backend/hsk_api/content/default_lesson.py`,
  `backend/hsk_api/services/lessons.py`, `backend/hsk_api/routers/`, backend dependency
  manifests and `backend/tests/test_lesson_api.py`.

## Task-2 — Add the server-side AI lesson adapter

- [x] Status: Complete
- Depends on: Task-1
- Goal: Add configurable OpenAI structured lesson generation behind an adapter and ensure
  every unavailable/error/invalid path selects fallback without exposing secrets.
- Files touched: `backend/hsk_api/config.py`, `backend/hsk_api/adapters/`,
  `backend/hsk_api/services/lessons.py`, backend adapter/service tests, `.env.example`.
- Definition of done: Backend tests pass for successful fake generation, missing key,
  timeout, provider failure and invalid schema; FR-14, FR-15 and FR-18 are covered.
- Implemented files: `backend/hsk_api/config.py`, `backend/hsk_api/adapters/`,
  `backend/hsk_api/services/lessons.py`, `.env.example`,
  `backend/tests/test_lesson_service.py`, `backend/tests/test_config.py` and
  `backend/tests/test_openai_adapter.py`.

## Task-3 — Scaffold Angular shell, API data layer and dashboard

- [x] Status: Complete
- Depends on: Task-1
- Goal: Create the Angular project, typed lesson contract, API service, responsive application
  shell and dashboard states with a route to the recommended lesson.
- Files touched: Angular workspace files, `frontend/src/app/core/`,
  `frontend/src/app/features/dashboard/`, `frontend/src/app/app.routes.ts`,
  `frontend/src/styles.scss`, `frontend/proxy.conf.json`, frontend tests.
- Definition of done: Angular tests and build pass; dashboard tests cover FR-1, FR-16 and
  FR-17.
- Implemented files: Angular 21 workspace, `frontend/src/app/core/models/lesson.ts`,
  `frontend/src/app/core/services/lesson-api.service.ts`,
  `frontend/src/app/features/dashboard/`, application shell/routes/styles,
  `frontend/proxy.conf.json` and related tests.

## Task-4 — Implement lesson overview

- [x] Status: Complete
- Depends on: Task-3
- Goal: Present goal, five-card count, duration, learning supports and an unambiguous start
  action using the loaded lesson.
- Files touched: `frontend/src/app/features/lesson-overview/`, routes and component tests.
- Definition of done: Angular tests pass and cover FR-2 plus the dashboard-to-overview
  transition in AC-1.
- Implemented files: `frontend/src/app/features/lesson-overview/` and the `/lesson` route.

## Task-5 — Implement session state and persistence

- [x] Status: Complete
- Depends on: Task-3
- Goal: Own reveal/rating rules, progress, result calculations, review-only sessions and
  browser-session restoration independently of UI.
- Files touched: `frontend/src/app/core/services/study-session.service.ts` and its tests.
- Definition of done: Service tests pass and cover FR-7 through FR-13, including restoration
  from session storage.
- Implemented files: `frontend/src/app/core/services/study-session.service.ts` and its
  five state-machine/persistence tests.

## Task-6 — Implement flip-card study screen

- [x] Status: Complete
- Depends on: Task-4, Task-5
- Goal: Render active recall, reveal details, rating actions, progress and error/empty states
  against the session service.
- Files touched: `frontend/src/app/features/study/`, route configuration and component tests.
- Definition of done: Angular tests pass and cover FR-4 through FR-9, FR-16 and FR-17.
- Implemented files: `frontend/src/app/features/study/` and the `/study` route.

## Task-7 — Implement results and immediate review flow

- [x] Status: Complete
- Depends on: Task-5, Task-6
- Goal: Present remembered/unremembered totals and review list, then route to review-only
  study or back to the dashboard.
- Files touched: `frontend/src/app/features/results/`, routes and component tests.
- Definition of done: Angular tests pass and cover FR-10 through FR-12 and AC-5/AC-6.
- Implemented files: `frontend/src/app/features/results/` and the `/results` route.

## Task-8 — Verify the full local learner journey

- [x] Status: Complete
- Depends on: Task-2, Task-7
- Goal: Run backend and frontend together and automate the complete five-card journey,
  including fallback behavior and same-session progress.
- Files touched: `frontend/e2e/`, E2E configuration and integration test helpers.
- Definition of done: E2E passes against the running local stack and covers AC-1 through
  AC-9; asset/response secret scan covers AC-10.
- Evidence: Playwright completes the five-card journey, result screen and two-card review
  flow against the local Angular/FastAPI stack; configuration tests and frontend bundle scan
  cover secret isolation.

## Task-9 — Add Vercel deployment configuration and operator documentation

- [x] Status: Complete
- Depends on: Task-2, Task-3
- Goal: Make both project roots buildable by Vercel and document safe environment setup,
  local commands, preview deployment and production deployment.
- Files touched: frontend/backend deployment configuration, `.gitignore`, `.env.example`,
  root `README.md`.
- Definition of done: Clean backend dependency install/tests and frontend production build
  pass; Vercel CLI build or equivalent local readiness checks pass without real secrets.
- Evidence: Python 3.12 clean-environment tests, Angular production build, JSON configuration
  validation and operator instructions pass. Vercel CLI local build is blocked by the
  documented host-specific `spawn cmd.exe ENOENT` issue; no deployment was performed.

## Task-10 — Update living architecture and run release-quality verification

- [x] Status: Complete
- Depends on: Task-8, Task-9
- Goal: Replace Planned architecture claims with verified current state and run the complete
  backend, frontend, integration and build verification suite.
- Files touched: `docs/architecture/Architecture.md`, task statuses and any verification
  documentation.
- Definition of done: Architecture matches the implemented tree; all required test/build
  commands pass from a clean invocation and every FR-1 through FR-18 maps to passing evidence.
- Evidence: Current-state architecture records implemented and deferred components. Fresh
  verification passes 13 backend tests, 15 frontend tests, the Angular production build and
  the complete Playwright journey; the plan traceability matrix maps FR-1 through FR-18.
