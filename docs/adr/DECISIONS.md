# Decision Log

The single, scannable index of every decision recorded in `docs/adr/`. Check here first
before opening individual ADR files. Appended to by `/spec:plan`, `/engineering:refactor`,
and `/decide` — every ADR gets a row here the moment it's written. New rows go at the top
(newest first, matching CHANGELOG.md's convention).

ADRs are identified by filename (`YYYY-MM-DD-slug.md`), not a sequential number — see
`README.md` in this folder for why. If two branches append a row at nearly the same time,
resolve the merge conflict here the normal way (keep both rows); there's no numbering to
reconcile since each ADR's identity is already unique.

| Date | Decision | Status | Supersedes | Affects |
|---|---|---|---|---|
| 2026-08-01 | [Dùng bài thi tổng kết làm điều kiện thăng cấp HSK](2026-08-01-level-exam-promotion-gate.md) | Accepted | Promotion decision in 2026-07-31-progressive-hsk-ai-paths | Checkpoints, daily paths, exams, progression |
| 2026-08-01 | [Thêm bài kiểm tra đầu vào thích ứng, tùy chọn](2026-08-01-optional-placement-test.md) | Accepted | Entry-level decision in 2026-07-31-beginner-first-learning-intelligence | Onboarding, profiles, daily paths, pronunciation |
| 2026-08-01 | [Server sở hữu nội dung phiên từ vựng theo chủ đề](2026-08-01-server-owned-topic-vocabulary.md) | Accepted | — | Topic recommendations, vocabulary sessions, profile progress, SRS |
| 2026-07-31 | [Dùng PostgreSQL cho persistence production](2026-07-31-postgresql-production-persistence.md) | Accepted | SQLite production trong 2026-07-31-user-accounts | Repository, accounts, profiles, AI paths, Vercel deployment |
| 2026-07-31 | [Bắt đầu HSK 1 và thêm learning intelligence có kiểm soát](2026-07-31-beginner-first-learning-intelligence.md) | Accepted | — | Onboarding, AI quality/cost, pronunciation, analytics, content admin |
| 2026-07-31 | [Dùng Ngày làm đơn vị trải nghiệm ngoài cùng](2026-07-31-learning-day-container.md) | Accepted | — | Daily path API, dashboard, checkpoints, progress terminology |
| 2026-07-31 | [Server sở hữu và lưu bất biến lộ trình AI](2026-07-31-server-owned-ai-paths.md) | Accepted | — | Daily path persistence, API, account deletion, synchronization |
| 2026-07-31 | [Lộ trình AI tăng dần từ HSK 1 đến HSK 6](2026-07-31-progressive-hsk-ai-paths.md) | Accepted | — | AI daily paths, HSK progression, checkpoints, dashboard |
| 2026-07-31 | [Dùng AI transcription cho phản hồi phát âm](2026-07-31-ai-pronunciation-feedback.md) | Accepted | — | Pronunciation API, lesson player, privacy, tests |
| 2026-07-31 | [Dùng tài khoản riêng và hồ sơ học trên máy chủ](2026-07-31-user-accounts.md) | Accepted | 2026-07-30-persistent-learning-loop | Authentication, learner profile, progress persistence, Angular routes |
| 2026-07-30 | [Dùng vòng học bền vững trên thiết bị cho người dùng ẩn danh](2026-07-30-persistent-learning-loop.md) | Accepted | — | Progress, SRS, streak, tests, vocabulary notebook |
| 2026-07-30 | [Dùng hợp đồng lesson API có cấu trúc](2026-07-30-lesson-api-contract.md) | Accepted | — | Backend API, Angular data layer, tests |
| 2026-07-30 | [Tách frontend và backend thành hai Vercel project](2026-07-30-separate-vercel-projects.md) | Accepted | — | Repository layout, local development, deployment |
| 2026-07-30 | [Sử dụng FastAPI, Angular và Vercel](2026-07-30-fastapi-angular-vercel.md) | Accepted | — | Architecture, implementation plans, deployment |
| 2026-07-30 | [Sử dụng AI API để tạo bài học phù hợp](2026-07-30-ai-generated-lessons.md) | Accepted | — | Vision, PRD, Architecture, lesson specifications |
