# Tasks: Lộ trình học theo Ngày
Plan: docs/specs/daily-learning-days/ImplementationPlan.md

## Task-1 — Hợp đồng metadata Ngày
- [x] Status: Completed
- Depends on: none
- Goal: API tổng quan trả Ngày liên tục với cấp, độ khó, phạm vi và trạng thái.
- Files touched: backend learning models/service/tests.
- Definition of done: backend tests phủ FR-1–4, FR-7, FR-9 và AC-1–2.

## Task-2 — Hành động tiến độ theo Ngày
- [x] Status: Completed
- Depends on: Task-1
- Goal: Chọn đúng Bài/checkpoint/tạo Ngày/hoàn tất mà không phụ thuộc ngày lịch.
- Files touched: frontend models, progress service/tests, lesson player tests.
- Definition of done: service tests phủ FR-9–13, FR-18 và AC-3–5.

## Task-3 — Dashboard nhóm Bài theo Ngày
- [x] Status: Completed
- Depends on: Task-1, Task-2
- Goal: Hiển thị Ngày hiện tại, Ngày hoàn thành, tiến độ x/5 và Bài đúng nhóm.
- Files touched: learning home component/template/styles/tests.
- Definition of done: component tests phủ FR-5–8, FR-14–15 và AC-6–8.

## Task-4 — Xác minh thích nghi và runtime
- [x] Status: Completed
- Depends on: Task-1, Task-2, Task-3
- Goal: Xác minh củng cố/tăng cấp, build và hành vi thật trên cổng 4204.
- Files touched: backend/frontend regression tests, task evidence, architecture.
- Definition of done: FR-16–18 và AC-9–10 được kiểm chứng; toàn bộ tests/build xanh.

## Verification evidence

- Backend: `40 passed` (`pytest -q`, 2026-07-31).
- Daily-path API: `9 passed`, bao gồm tiếp tục nhiều Ngày trong cùng ngày lịch, tăng dần đến HSK 6
  và kết thúc hành trình sau khi hoàn thành HSK 6.
- Frontend: `25` test files, `66 passed` (`ng test --watch=false`, 2026-07-31).
- Production build: `ng build` thành công, không có cảnh báo budget.
- Runtime trên `http://127.0.0.1:4204/learn`: Ngày 2 hiện trước Ngày 1 đã hoàn thành; Bài 6 mở
  đúng nội dung; Bài 1–5 vẫn có thể học lại; checkpoint Ngày 2 còn khóa ở tiến độ 0/5.
- Acceptance audit: AC-1–AC-10 đạt; FR-1–FR-18 có test tự động hoặc kiểm chứng runtime tương ứng.
