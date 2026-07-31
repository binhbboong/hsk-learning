# Tasks: Tài khoản người học
Plan: docs/specs/user-accounts/ImplementationPlan.md

## Task-1 — Account storage and security
- [x] Status: Complete — account hashing/session API tests pass.
- Depends on: none
- Goal: Store accounts, hashed passwords and revocable sessions.
- Definition of done: API tests cover FR-1–FR-5.

## Task-2 — Per-user learning profile API
- [x] Status: Complete — two-account API isolation tests pass.
- Depends on: Task-1
- Goal: Read and update only the authenticated learner's profile.
- Definition of done: isolation tests cover FR-8–FR-10.

## Task-3 — Frontend authentication domain
- [x] Status: Complete — auth service, session restore and route protection tests pass.
- Depends on: Task-1
- Goal: Maintain session, protect routes and handle expiry.
- Definition of done: service, interceptor and guard tests cover FR-5, FR-6 and FR-12.

## Task-4 — Friendly authentication UI
- [x] Status: Complete — login/register validation and submit states pass.
- Depends on: Task-3
- Goal: Build accessible register/login states from authentication.md.
- Definition of done: component tests cover FR-1, FR-3, FR-7 and FR-11.

## Task-5 — Account-aware profile sync and navigation
- [x] Status: Complete — local import, server sync, account menu and logout are implemented.
- Depends on: Task-2, Task-3
- Goal: Import anonymous progress, sync changes, show account and log out.
- Definition of done: tests cover FR-7–FR-10.

## Task-6 — Full verification
- [x] Status: Complete — 27 backend, 54 frontend and 7 E2E tests plus build/browser QA pass.
- Depends on: Task-1–Task-5
- Goal: Verify two-user isolation, responsiveness and live port 4204.
- Definition of done: backend, frontend, build, E2E and browser checks pass.
