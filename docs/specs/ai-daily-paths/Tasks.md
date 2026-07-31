# Tasks: Lộ trình hằng ngày do AI tạo
Plan: docs/specs/ai-daily-paths/ImplementationPlan.md

## Task-1 — Hợp đồng và persistence cho chặng động
- [x] Status: Completed
- Depends on: none
- Goal: Mô hình hóa và lưu chặng 5 bài bất biến theo tài khoản/chỉ số.
- Files touched: models learning loop, account repository, repository tests.
- Definition of done: persistence tests chứng minh lưu/đọc/idempotency và FR-1, FR-7,
  FR-8, FR-11, FR-15.

## Task-2 — Generator AI và kiểm định độ khó HSK
- [x] Status: Completed
- Depends on: Task-1
- Goal: Tạo bundle 5 bài + checkpoint theo cấp, difficulty và learner context.
- Files touched: OpenAI daily-path adapter, daily-path service, service tests.
- Definition of done: generator/service tests phủ FR-3, FR-4, FR-9, FR-10, FR-18–24,
  FR-26–28.

## Task-3 — API lộ trình động
- [x] Status: Completed
- Depends on: Task-1, Task-2
- Goal: Trả tổng quan hợp nhất, bài/checkpoint theo phạm vi và tạo chặng kế tiếp an toàn.
- Files touched: learning-path router, app composition, backend API tests.
- Definition of done: API tests phủ AC-1–8 và AC-11–15.

## Task-4 — Data layer và progress động trên frontend
- [x] Status: Completed
- Depends on: Task-3
- Goal: Loại bỏ giả định 5 bài toàn lộ trình và tính đúng bài/checkpoint/chặng tiếp theo.
- Files touched: learning-content models, learning-path API service, progress service/tests.
- Definition of done: service tests phủ FR-5, FR-12, FR-16–17, FR-23–28.

## Task-5 — Dashboard và checkpoint nhiều chặng
- [x] Status: Completed
- Depends on: Task-4
- Goal: Hiển thị cấp/chặng, tạo chặng, lỗi/thử lại và checkpoint đúng phạm vi.
- Files touched: learning home, checkpoint component, templates/styles/specs.
- Definition of done: component tests phủ FR-12–14, FR-16, FR-25 và wireframe states.

## Task-6 — Xác minh tích hợp và cập nhật kiến trúc hiện trạng
- [x] Status: Completed
- Depends on: Task-1, Task-2, Task-3, Task-4, Task-5
- Goal: Xác minh backend/frontend/runtime và chuyển planned architecture thành implemented.
- Files touched: Architecture.md, task statuses, regression tests.
- Definition of done: toàn bộ backend/frontend tests và builds xanh; runtime tạo/lấy chặng
  tiếp theo đúng; AC-1–15 có bằng chứng.

## Verification evidence

- Backend: `36 passed`.
- Frontend: `63 passed`.
- Production build: Angular build completed successfully.
- Runtime: account path persisted Bài 6–10, dashboard showed `5 / 10 bài`,
  `HSK 1 · độ khó 2/5`, and Bài 6 loaded all four learning activities.
