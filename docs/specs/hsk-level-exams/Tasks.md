# Tasks: Bài thi tổng kết cấp HSK
Plan: docs/specs/hsk-level-exams/ImplementationPlan.md

## Task-1 — Domain và blueprint
- [x] Status: Completed
- Depends on: none
- Goal: Mô hình hóa đề 20 câu và fallback HSK 1 không lộ đáp án.
- Files touched: level-exam models/content/tests.
- Definition of done: test blueprint và privacy đạt; FR-4–FR-8.

## Task-2 — Persistence và attempt service
- [x] Status: Completed
- Depends on: Task-1
- Goal: Lưu đề/lượt, chọn câu, đánh dấu, resume và nộp bài.
- Files touched: repository, level-exam service/tests.
- Definition of done: persistence/scoring/retake tests đạt; FR-9–FR-14, FR-17–FR-19.

## Task-3 — API và audio
- [x] Status: Completed
- Depends on: Task-2
- Goal: Cung cấp status/start/save/submit/audio API có auth và lỗi rõ ràng.
- Files touched: router, main, API tests.
- Definition of done: API contract tests đạt; FR-7–FR-12, FR-20.

## Task-4 — Gate thăng cấp
- [x] Status: Completed
- Depends on: Task-2
- Goal: Yêu cầu thi khi đã mastery và chỉ thăng cấp sau khi đạt.
- Files touched: daily-path service/models/router/tests.
- Definition of done: HSK 1–5 và HSK 6 promotion tests đạt; FR-1–FR-3, FR-15–FR-16.

## Task-5 — Giao diện bài thi
- [x] Status: Completed
- Depends on: Task-3
- Goal: Triển khai intro, runner, review markers, submit và result responsive.
- Files touched: Angular models/service/feature/routes/tests.
- Definition of done: component/service tests phủ mọi state wireframe; FR-10–FR-17, FR-20.

## Task-6 — Dashboard và regression
- [x] Status: Completed
- Depends on: Task-4, Task-5
- Goal: Nối hành động thi vào lộ trình và xác minh không đổi streak/SRS.
- Files touched: progress/home/tests/docs.
- Definition of done: full suites, build và browser QA đạt; FR-1, FR-15, FR-18.
