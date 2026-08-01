# Tasks: Học thích nghi và vận hành nội dung
Plan: docs/specs/learning-intelligence-operations/ImplementationPlan.md

## Task-1 — Quality gate, quota và usage
- [x] Status: Completed
- Depends on: none
- Goal: Chặn bundle sai/trùng, giới hạn lượt tạo và ghi usage.
- Files touched: backend content models/services/repository/daily path tests.
- Definition of done: tests đỏ-xanh phủ FR-2–6 và AC-2–3.

## Task-2 — Quy trình quản trị nội dung
- [x] Status: Completed
- Depends on: Task-1
- Goal: Admin xem, sửa, duyệt và từ chối draft; người học chỉ thấy nội dung phát hành.
- Files touched: backend admin router/repository/tests.
- Definition of done: tests đỏ-xanh phủ FR-7–10 và AC-4.

## Task-3 — Phân tích phát âm theo âm tiết
- [x] Status: Completed
- Depends on: none
- Goal: Trả quan sát âm tiết/thanh điệu, mẹo Việt và disclaimer.
- Files touched: pronunciation model/adapter/router/frontend service/player/tests.
- Definition of done: tests đỏ-xanh phủ FR-11–13 và AC-5.

## Task-4 — Analytics 7/30 ngày và gợi ý ôn
- [x] Status: Completed
- Depends on: none
- Goal: Tổng hợp hoạt động, retention, điểm yếu và một hành động ưu tiên.
- Files touched: profile model/repository, analytics service/router/tests.
- Definition of done: tests đỏ-xanh phủ FR-14–18 và AC-6.

## Task-5 — Dashboard insight
- [x] Status: Completed
- Depends on: Task-4
- Goal: Hiển thị insight mà không chặn lộ trình khi analytics lỗi.
- Files touched: learning-home component/template/styles/tests, analytics client.
- Definition of done: tests đỏ-xanh phủ FR-15–19 và AC-6–7.

## Task-6 — Giao diện quản trị và audit
- [x] Status: Completed
- Depends on: Task-2
- Goal: Hoàn thiện màn quản trị, cấu hình admin và xác minh toàn hệ thống.
- Files touched: Angular admin feature/routes/tests, config docs, architecture.
- Definition of done: AC-1–8 đạt; toàn bộ backend/frontend tests và build xanh.

## Verification evidence

- Backend: toàn bộ `47 passed` (bao gồm adapter WAV và nhánh bỏ qua WebM không hỗ trợ).
- Frontend: `27` test files, toàn bộ `71 passed` (bao gồm bộ mã hóa PCM16 WAV).
- Production build: Angular build thành công, không còn cảnh báo budget.
- Runtime: tài khoản mới có thể bỏ qua bài đầu vào để vào `HSK 1`, `Ngày 1`, độ khó `1/5`.
- Runtime: dashboard hiển thị hoạt động 7 ngày, ghi nhớ 30 ngày, điểm yếu và một hành động đề xuất.
- Dữ liệu tài khoản QA tạm thời đã được xóa sau khi kiểm tra.
- Runtime sau restart: frontend `4204` trả HTTP 200; backend `8010/api/health` trả HTTP 200.
