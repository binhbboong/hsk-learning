# Architecture: HSK Learning

PRD: docs/business/PRD.md  
Last updated: 2026-07-31  
Status: Implemented for account-specific AI learning paths

## Implemented learning intelligence and content operations

This update supersedes older deferred statements retained later in this document. Every new account
starts at HSK 1, difficulty 1, without a placement test. Progression still uses completed five-lesson
groups and checkpoints from the daily-path architecture.

AI path generation now passes through schema, HSK-scope, completeness and repetition quality gates.
Per-account and system-wide daily quotas are configurable. Token usage, model status and generated
drafts are persisted. A failed or repetitive bundle is not published; it enters the admin review queue.
Quality-passing bundles are auto-approved so the learner's next day remains continuous. Configured
admins can inspect usage and edit, approve or reject drafts through `/admin/content`.

Learning profiles now contain activity events. `GET /api/v1/analytics/learning` derives a seven-day
activity view, 30-day vocabulary retention, the current skill weakness and one prioritized action.
Analytics failure is isolated from the core learning-path request and never blocks the next lesson.

Pronunciation analysis combines unbiased Chinese transcription with `gpt-audio` acoustic feedback.
The browser converts MediaRecorder output to PCM16 WAV before upload because model audio input accepts
WAV/MP3. The response contains content score, per-syllable target, tone, status and a Vietnamese tip.
If audio analysis is unavailable, the API returns an explicit uncertain fallback and always displays
that AI feedback is practice support rather than an exam or teacher assessment.

Implemented additional API boundaries:

- `GET /api/v1/analytics/learning`
- `GET /api/v1/admin/content`
- `GET /api/v1/admin/usage`
- `PUT /api/v1/admin/content/{id}`
- `POST /api/v1/admin/content/{id}/approve`
- `POST /api/v1/admin/content/{id}/reject`

## Implemented AI daily-path expansion

The learner-facing container is **Ngày** (Day): exactly five continuously-numbered lessons and
one checkpoint. `path_index` remains an internal persistence identity. The aggregate path API
exposes Day metadata so clients do not reconstruct level, difficulty or checkpoint state.

The approved `ai-daily-paths` specification extends the current five-lesson HSK 1 slice into
server-owned, account-specific groups of five lessons plus a checkpoint. Generated groups
remain immutable, use continuous lesson numbering and progressively cover HSK 1 through
HSK 6. Promotion requires at least 80% on the level checkpoint and 70% vocabulary retention.
The first static HSK 1 group remains the entry point. After each completed checkpoint, FastAPI
evaluates checkpoint and vocabulary-retention thresholds, generates or reinforces the appropriate
HSK level, validates the full multi-activity bundle and persists it in SQLite. Angular then reloads
the aggregate path and continues at the next continuous lesson number.

Implemented API boundary:

- `GET /api/v1/path`
- `GET /api/v1/path/lessons/{number}`
- `GET /api/v1/path/checkpoint?start={number}`
- `POST /api/v1/path/next`

`POST /next` is authenticated and idempotent for the active generated group. AI failures never
persist partial content and the dashboard exposes a Vietnamese retry state.

Related decisions:

- [Progressive HSK AI paths](../adr/2026-07-31-progressive-hsk-ai-paths.md)
- [Server-owned AI paths](../adr/2026-07-31-server-owned-ai-paths.md)

## Account and server-profile update

Authentication is now implemented with email/password accounts, revocable bearer sessions and
per-account learning profiles. FastAPI stores accounts, `scrypt` password hashes, hashed session
tokens and profile payloads in SQLite. Angular protects `/learn/**`, restores the active session,
imports existing anonymous progress into an empty account, synchronizes later profile changes and
clears browser learning state on logout.

Current account endpoints:

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/logout`
- `GET /api/v1/profile`
- `PUT /api/v1/profile`

This section supersedes the anonymous-only and deferred-authentication statements retained below as
historical architecture context.

## Persistent learning loop update

The initial HSK 1 slice includes a five-lesson learning path. Each lesson combines sentence-level
dialogue audio, independent Pinyin/translation controls, listening multiple choice, sentence ordering,
pronunciation recording/playback, and personal vocabulary saving. The fifth completed lesson unlocks a
mixed checkpoint.

Anonymous learner state is stored in a versioned `localStorage` profile
(`hsk-learning.profile.v1`). It contains completed lesson IDs, streak state, SRS cards, unresolved
mistakes, notebook words, and checkpoint results. Microphone recordings remain ephemeral browser blob
URLs and are never persisted.

The Angular `/learn` area prioritizes the current unlocked checkpoint, due SRS reviews and the next
unfinished lesson. Once a group checkpoint is complete, it automatically requests the next five
lessons. The heading exposes current HSK level, group difficulty and cumulative lesson progress.

## Overview

HSK Learning hiện có một vertical slice chạy được gồm Angular 21, FastAPI và cấu hình triển
khai thành hai Vercel project độc lập. MVP phục vụ người mới học HSK 1 bằng bốn loại bài:
từ vựng flip-card, ngữ pháp tương tác, nghe hiểu và phát âm. Nội dung từ vựng có thể được
tạo bởi OpenAI ở phía máy chủ; toàn bộ bài mới dùng nội dung HSK 1 đã kiểm duyệt.

## Components

| Component | Status | Responsibility and boundary | Serves epics |
|---|---|---|---|
| Angular web application | Implemented | Dashboard, catalog bốn kỹ năng, flip-card, ngữ pháp, nghe, ghi âm phát âm và kết quả; không chứa bí mật hoặc gọi trực tiếp OpenAI. | Epic-1, Epic-2, Epic-3, Epic-5, Epic-6 |
| FastAPI application API | Implemented | Cung cấp health check, recommended vocabulary lesson, skill catalog và nội dung ba bài kỹ năng; điều phối AI/fallback và CORS. | Epic-1 đến Epic-6 |
| Learning content domain | Implemented for HSK 1 MVP | Mô hình 5 thẻ từ vựng, mẫu câu/câu hỏi, đoạn nghe và hướng dẫn thanh điệu dành cho người Việt. | Epic-1, Epic-2, Epic-3, Epic-6 |
| AI lesson adapter | Implemented | Dùng OpenAI Responses API với structured output, timeout và kiểm tra schema; API key chỉ tồn tại phía máy chủ. | Epic-4 |
| Browser audio adapter | Implemented | Dùng speech synthesis cho audio tiếng Trung, MediaRecorder để ghi/nghe lại và chuyển bản ghi sang WAV khi người học yêu cầu AI phân tích. | Epic-3, Epic-6 |
| Session progress storage | Implemented | Angular services quản lý flip-card, kết quả kỹ năng, ôn lại và khôi phục bằng `sessionStorage`. | Epic-1, Epic-2, Epic-3, Epic-5 |
| Persistent learner storage | Deferred | Chưa có tài khoản, đồng bộ nhiều thiết bị hoặc lưu dữ liệu dài hạn. | Epic-5 |
| Deployment configuration | Implemented | Build frontend/backend, cấu hình biến môi trường và SPA routing cho hai Vercel project. | Tất cả epics |

## Current Data Flows

1. Angular gọi `GET /api/v1/lessons/recommended?level=1&size=5`.
2. FastAPI yêu cầu AI adapter tạo đúng năm thẻ khi có `OPENAI_API_KEY`.
3. Kết quả AI phải vượt qua Pydantic schema. Thiếu key, timeout, lỗi nhà cung cấp hoặc dữ
   liệu sai đều chuyển sang bài HSK 1 fallback.
4. Angular giữ bài học và trạng thái phiên trong trình duyệt. Người học phải lật thẻ trước
   khi chọn “Đã nhớ” hoặc “Chưa nhớ”.
5. Sau thẻ cuối, Angular tính kết quả và tạo một phiên ôn chỉ gồm các thẻ chưa nhớ.
6. Catalog kỹ năng tải từ `/api/v1/skills`; ba lesson endpoint trả nội dung ngữ pháp, nghe
   và phát âm đã kiểm duyệt.
7. Audio mẫu được tổng hợp trên trình duyệt. Bản ghi microphone có blob URL tạm để nghe lại; chỉ khi
   người học chọn phân tích AI, bản WAV mới được gửi tới FastAPI và không được lưu lâu dài.
8. Mỗi lesson tạo kết quả dùng chung, lưu trong phiên để hỗ trợ học lại hoặc chọn kỹ năng khác.

Không có dữ liệu tiến độ hoặc API key nào được gửi tới kho lưu trữ lâu dài trong MVP.

## Cross-Cutting Decisions

- Authentication: chưa có trong MVP; cần ADR mới trước khi thêm tài khoản.
- Authentication update: [ADR user accounts](../adr/2026-07-31-user-accounts.md) supersedes the
  statement above.
- Persistence: `sessionStorage` chỉ phục vụ khôi phục trong cùng phiên trình duyệt.
- AI integration: [ADR AI-generated lessons](../adr/2026-07-30-ai-generated-lessons.md).
- API contract: [ADR lesson API contract](../adr/2026-07-30-lesson-api-contract.md).
- Persistent learning profile: [ADR persistent learning loop](../adr/2026-07-30-persistent-learning-loop.md).
- Deployment stack: [ADR FastAPI/Angular/Vercel](../adr/2026-07-30-fastapi-angular-vercel.md).
- Deployment topology: [ADR separate Vercel projects](../adr/2026-07-30-separate-vercel-projects.md).
- Secrets: API key chỉ được đọc từ biến môi trường phía FastAPI và không xuất hiện trong
  response hay frontend bundle.

## Deployment Topology

- Frontend project root: `frontend`; production output: `dist/frontend/browser`.
- Backend project root: `backend`; Vercel entrypoint: `app.py`.
- Frontend nhận URL backend từ `API_BASE_URL` tại build time.
- Backend nhận danh sách origin frontend từ `CORS_ORIGINS`.
- Local development dùng Angular proxy để giữ cùng hợp đồng `/api`.

## Known Constraints / Technical Debt

- Nội dung tĩnh mới bao phủ chặng HSK 1 đầu tiên; các chặng tiếp theo HSK 1–6 phụ thuộc
  cấu hình OpenAI và vẫn cần theo dõi chất lượng.
- Không có bài kiểm tra đầu vào theo quyết định beginner-first. Phản hồi phát âm AI chỉ mang tính hỗ
  trợ luyện tập; số liệu ghi nhớ 30 ngày chỉ có ý nghĩa sau khi người học tích lũy đủ hoạt động.
- Chất lượng speech synthesis phụ thuộc voice tiếng Trung có trên thiết bị; UI có transcript
  fallback khi audio hoặc microphone không khả dụng.
- Nội dung AI vẫn cần quan sát chất lượng và quy trình biên tập trước khi mở rộng.
- Vercel CLI trên máy hiện tại gặp lỗi môi trường `spawn cmd.exe ENOENT`; production build,
  dependency install, test và cấu hình deploy được kiểm tra độc lập, nhưng preview deployment
  vẫn cần chạy trên Vercel hoặc một máy CLI không gặp lỗi này.
