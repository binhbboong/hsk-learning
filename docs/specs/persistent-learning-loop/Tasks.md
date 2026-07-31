# Tasks: Vòng học bền vững
Plan: docs/specs/persistent-learning-loop/ImplementationPlan.md

## Task-1 — Add five-lesson content contract
- [x] Status: Complete — 4 backend API tests pass.
- Depends on: none
- Goal: Expose five HSK 1 lessons and checkpoint content.
- Files touched: backend learning-loop models/content/router/tests.
- Definition of done: backend tests cover FR-1, FR-4, FR-6, FR-21 and FR-22.

## Task-2 — Add versioned learning profile repository
- [x] Status: Complete — repository restore/corruption tests pass.
- Depends on: none
- Goal: Persist and safely restore one anonymous profile.
- Files touched: profile model/repository/tests.
- Definition of done: tests cover FR-24, FR-25 and FR-26.

## Task-3 — Add progress, streak and checkpoint domain
- [x] Status: Complete — progress, streak and checkpoint tests pass.
- Depends on: Task-2
- Goal: Track lesson completion, next action, streak and five-lesson gates.
- Files touched: progress/streak services and tests.
- Definition of done: tests cover FR-17 through FR-23 and FR-27.

## Task-4 — Add SRS, mistake and notebook domain
- [x] Status: Complete — SRS, mistake and notebook tests pass.
- Depends on: Task-2
- Goal: Schedule reviews, resolve wrong answers and manage personal words.
- Files touched: SRS/mistake/notebook services and tests.
- Definition of done: tests cover FR-9 through FR-16.

## Task-5 — Build progress dashboard
- [x] Status: Complete — dashboard component test passes.
- Depends on: Task-1, Task-3, Task-4
- Goal: Present streak, progress and prioritized next action.
- Files touched: learning-home feature/routes/tests.
- Definition of done: component tests cover FR-18 and FR-27.

## Task-6 — Build multi-activity lesson player
- [x] Status: Complete — lesson player component tests pass.
- Depends on: Task-1, Task-3, Task-4
- Goal: Complete dialogue, listening, reorder, recording and save-word flow.
- Files touched: lesson-player feature/tests.
- Definition of done: tests cover FR-1 through FR-10 and AC-1 through AC-4.

## Task-7 — Build review center and notebook
- [x] Status: Complete — review and notebook component tests pass.
- Depends on: Task-4
- Goal: Review due cards/wrong answers and manage saved vocabulary.
- Files touched: review-center/notebook features/tests.
- Definition of done: tests cover FR-9 through FR-16 and AC-4/AC-5.

## Task-8 — Build five-lesson checkpoint
- [x] Status: Complete — checkpoint locking, score and mistake tests pass.
- Depends on: Task-1, Task-3, Task-4
- Goal: Complete mixed checkpoint and route errors to review.
- Files touched: checkpoint feature/tests.
- Definition of done: tests cover FR-21 through FR-23 and AC-6/AC-7.

## Task-9 — Verify persistence and full learning loop
- [x] Status: Complete — 22 backend tests, 49 frontend tests, production build, 6 E2E flows and live-browser QA pass.
- Depends on: Task-1 through Task-8
- Goal: Run fresh unit/build/E2E/browser verification and update architecture.
- Files touched: E2E, architecture and task evidence.
- Definition of done: AC-1 through AC-8 have fresh evidence.
