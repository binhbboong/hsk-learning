# Tasks: Phiên từ vựng chủ đề bắt buộc theo Ngày
Plan: docs/specs/mandatory-daily-topic-vocabulary/ImplementationPlan.md

## Task-1 — Metadata và gate phía server
- [x] Status: Completed
- Depends on: none
- Goal: Mỗi Ngày có trạng thái phiên chủ đề và API không tạo Ngày kế tiếp khi còn thiếu.
- Files touched: backend learning model, daily path service và API tests.
- Definition of done: backend tests pass, FR-1 và FR-4–9 được phủ.

## Task-2 — Hành động tiếp theo và dashboard
- [x] Status: Completed
- Depends on: Task-1
- Goal: Sau 5 Bài, dashboard bắt buộc dẫn tới phiên 10 từ trước khi mở checkpoint.
- Files touched: frontend learning model, progress service, learning home và tests.
- Definition of done: frontend tests pass, FR-2–5 và FR-7–8 được phủ.

## Task-3 — Hoàn thành phiên và quay về lộ trình
- [x] Status: Completed
- Depends on: Task-2
- Goal: Phiên bắt buộc hoàn thành có đường quay lại checkpoint rõ ràng và giữ SRS/streak.
- Files touched: topic vocabulary component/session tests.
- Definition of done: frontend tests pass, FR-10–12 được phủ.

## Task-4 — Xác minh tích hợp và production
- [x] Status: Completed
- Depends on: Task-1, Task-2, Task-3
- Goal: Xác minh trọn luồng 5 Bài → 10 từ → checkpoint → Ngày kế tiếp.
- Files touched: regression tests, task evidence và tài liệu kiến trúc nếu cần.
- Definition of done: AC-1–AC-8 đạt; backend/frontend suites và production build xanh.

## Verification evidence — 2026-08-03

- Backend: `76 passed, 1 skipped`.
- Frontend: `102 passed`.
- Production build: Angular build completed successfully.
