# Implementation Plan: Phiên từ vựng chủ đề bắt buộc theo Ngày
Spec: docs/specs/mandatory-daily-topic-vocabulary/Specification.md

## Approach

### Chọn: server phân bổ phiên hoàn thành theo thứ tự Ngày, client hiển thị và điều hướng

Server đếm các phiên chủ đề đã hoàn thành trong hồ sơ và phân bổ tuần tự, mỗi phiên cho tối đa một
Ngày. Metadata Ngày trả trực tiếp trạng thái bước chủ đề. Điều kiện tạo Ngày kế tiếp dùng cùng phép
tính để không thể bỏ qua bằng cách gọi API trực tiếp. Frontend dựa trên metadata này để chọn hành
động 5 Bài → 10 từ → checkpoint.

Các phương án đã cân nhắc:

1. Chỉ khóa checkpoint ở frontend: ít thay đổi nhưng có thể bỏ qua qua API và tạo trạng thái lệch.
2. Gắn số Ngày mới vào từng phiên: chính xác hơn cho dữ liệu mới nhưng cần thay đổi vòng đời session
   và migration phức tạp cho phiên cũ.
3. Phân bổ tuần tự trên server (chọn): một nguồn sự thật, tương thích hồ sơ hiện có và đủ chặt cho MVP.

## File/Module Structure

| Path | Responsibility | Implements |
|---|---|---|
| `backend/hsk_api/models/learning_loop.py` | Trạng thái bước chủ đề trong metadata Ngày | FR-1, FR-7–8 |
| `backend/hsk_api/services/daily_paths.py` | Phân bổ phiên và khóa tạo Ngày kế tiếp | FR-4–9 |
| `backend/tests/test_daily_paths_api.py` | Kiểm thử hợp đồng, hoàn thành và gate server | FR-4–9 |
| `frontend/src/app/core/models/learning-content.ts` | Kiểu trạng thái chủ đề của Ngày | FR-7 |
| `frontend/src/app/core/services/progress.service.ts` | Chọn hành động 5 Bài → chủ đề → checkpoint | FR-3–5, FR-8 |
| `frontend/src/app/features/learning-home/*` | Hiển thị bước bắt buộc và trạng thái khóa | FR-1–4, FR-7–8 |
| `frontend/src/app/features/topic-vocabulary/*` | Hành động quay lại lộ trình sau phiên | FR-2, FR-10–12 |

## Testing Strategy

| Requirement | Verified by |
|---|---|
| FR-1, FR-7–8 | API schema tests và component tests cho ba bước của Ngày |
| FR-2–5 | Progress/component tests cho CTA chủ đề và checkpoint khóa/mở |
| FR-6, FR-9 | Backend tests với nhiều Ngày và nhiều phiên hoàn thành |
| FR-10–12 | Topic session regression tests và completion component test |

## Risks / Open Questions

- Phiên học trước khi thay đổi có thể được tính cho Ngày đầu tiên; đây là chủ đích tương thích dữ liệu.
- Người học có thể hoàn thành nhiều phiên độc lập trước; mỗi phiên vẫn chỉ đáp ứng một Ngày theo thứ tự.
- Không có open question chặn triển khai.

## Related ADRs

- docs/adr/2026-08-03-mandatory-daily-topic-vocabulary.md
- docs/adr/2026-07-31-learning-day-container.md
- docs/adr/2026-08-01-server-owned-topic-vocabulary.md
