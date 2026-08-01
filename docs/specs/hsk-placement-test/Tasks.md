# Tasks: HSK Placement Test

Status: Ready
Date: 2026-08-01

- [x] T1 — Add failing backend tests for question privacy, adaptive sequencing and scoring.
- [x] T2 — Add placement domain models, curated bank and `PlacementService`.
- [x] T3 — Add failing repository tests, schema and persistence for attempts/results.
- [x] T4 — Add failing API tests and placement routes including pronunciation upload.
- [x] T5 — Add failing daily-path tests for placement-selected `path_index=1` and atomic apply.
- [x] T6 — Implement profile starting level and daily-path integration without progress mutation.
- [x] T7 — Add failing Angular service/component tests for intro, runner, resume and result states.
- [x] T8 — Implement placement API client, route, responsive UI and theme styles.
- [x] T9 — Add conditional dashboard CTA and advisory retake entry.
- [x] T10 — Run backend/frontend suites and production build; fix regressions.
- [x] T11 — Browser QA entry/adaptive/resume/dashboard; API and component QA completion,
  apply, skip and failure paths.

## Files touched

- Backend: `models/placement.py`, `content/placement_test.py`, `services/placement.py`,
  `routers/placement.py`, account repository/profile and daily-path integration.
- Frontend: placement models/API, `/learn/placement`, learning-home entry and profile migration.
- Evidence: API flow and daily-path regression tests; Angular component/service tests; browser resume QA.
