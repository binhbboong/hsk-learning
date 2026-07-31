# Tasks: Bài học ngữ pháp, nghe và phát âm
Plan: docs/specs/integrated-language-skills/ImplementationPlan.md

## Task-1 — Add skills content API

- [x] Status: Complete
- Depends on: none
- Goal: Expose validated HSK 1 catalog and three skill lessons.
- Files touched: backend skills models, content, router and tests.
- Definition of done: backend tests pass and cover FR-1–FR-3, FR-6–FR-18 content contracts.
- Evidence: `backend/tests/test_skills_api.py` validates catalog, all lesson contracts and
  HSK 1 scope.

## Task-2 — Add typed client data layer and catalog

- [x] Status: Complete
- Depends on: Task-1
- Goal: Load and display four skill choices with all UI states.
- Files touched: client models/API service, catalog feature, dashboard route and tests.
- Definition of done: frontend tests pass and cover FR-1, FR-2 and FR-17.
- Evidence: API service and catalog component tests cover routes plus error/retry state.

## Task-3 — Implement interactive grammar lesson

- [x] Status: Complete
- Depends on: Task-1, Task-2
- Goal: Teach one pattern and complete two gated questions with feedback.
- Files touched: grammar feature and tests.
- Definition of done: frontend tests pass and cover FR-3 through FR-5.
- Evidence: grammar tests cover examples, answer gating, feedback and completion.

## Task-4 — Implement listening lesson

- [x] Status: Complete
- Depends on: Task-1, Task-2
- Goal: Play normal/slow audio, gate transcript and evaluate one answer.
- Files touched: audio service, listening feature and tests.
- Definition of done: frontend tests pass and cover FR-6 through FR-9.
- Evidence: listening tests cover playback rates, transcript gate, answer and audio fallback.

## Task-5 — Implement pronunciation coach

- [x] Status: Complete
- Depends on: Task-1, Task-2, Task-4
- Goal: Play sample, record/playback locally, support permission fallback and self-rating.
- Files touched: audio service, pronunciation feature and tests.
- Definition of done: frontend tests pass and cover FR-10 through FR-15.
- Evidence: pronunciation tests cover guidance, recording, fallback and self-rating.

## Task-6 — Implement shared skill result

- [x] Status: Complete
- Depends on: Task-3, Task-4, Task-5
- Goal: Summarize each skill and provide retry/catalog actions.
- Files touched: result service/component, routes and tests.
- Definition of done: frontend tests pass and cover FR-16 and AC-6.
- Evidence: result test covers score, feedback, retry and catalog actions.

## Task-7 — Verify integrated journeys and update living architecture

- [x] Status: Complete
- Depends on: Task-1 through Task-6
- Goal: Automate all three journeys and align current-state documentation.
- Files touched: E2E tests, architecture and task evidence.
- Definition of done: full backend/frontend/build/E2E suite passes and AC-1 through AC-7 map
  to fresh evidence.
- Evidence: Playwright covers vocabulary plus all three new skills; architecture records the
  expanded current state.
