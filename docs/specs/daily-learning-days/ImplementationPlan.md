# Implementation Plan: Lộ trình học theo Ngày
Spec: docs/specs/daily-learning-days/Specification.md

## Approach

### Chọn: metadata Ngày do server tính, giao diện chỉ trình bày

Giữ persistence `daily_paths` và `path_index` để tương thích dữ liệu. Server dựng danh sách
Ngày từ chặng tĩnh và các bundle đã lưu, sau đó tính tiến độ/checkpoint từ hồ sơ tài khoản.
Frontend dùng trực tiếp metadata này để nhóm Bài và hiển thị trạng thái.

Các phương án đã cân nhắc:

1. Frontend tự chia mảng Bài mỗi 5 phần tử: ít thay đổi backend nhưng lặp logic checkpoint,
   cấp và trạng thái; dễ sai khi hợp đồng thay đổi.
2. Đổi tên bảng và migration toàn bộ sang `learning_days`: rõ tên nhưng rủi ro dữ liệu không
   cần thiết, không tạo thêm giá trị cho người học.
3. Server tính metadata Ngày, giữ persistence hiện tại (chọn): hợp đồng rõ, tương thích dữ liệu
   và một nguồn sự thật cho web hoặc client tương lai.

## File/Module Structure

| Path | Responsibility | Implements |
|---|---|---|
| `backend/hsk_api/models/learning_loop.py` | Hợp đồng tổng quan và metadata Ngày | FR-1–4 |
| `backend/hsk_api/services/daily_paths.py` | Dựng Ngày, tiến độ và checkpoint từ dữ liệu lưu | FR-2–4, FR-7–11, FR-16–18 |
| `backend/tests/test_daily_paths_api.py` | Kiểm định hợp đồng Ngày và mở Ngày kế tiếp | AC-1–10 |
| `frontend/src/app/core/models/learning-content.ts` | Kiểu dữ liệu Ngày từ API | FR-4 |
| `frontend/src/app/core/services/progress.service.ts` | Chọn hành động tiếp theo theo Ngày | FR-5, FR-9–13, FR-18 |
| `frontend/src/app/features/learning-home/*` | Dashboard nhóm Bài theo Ngày và đủ trạng thái | `daily-learning-days.md`; FR-5–8, FR-14–15 |
| `frontend/src/app/features/lesson-player/*` | Chuyển đúng checkpoint cuối Ngày | `continuous-lessons.md`; FR-3, FR-9 |

## Testing Strategy

| Requirement | Verified by |
|---|---|
| FR-1–4 | Backend schema/API tests kiểm tra Ngày 1–2, phạm vi và metadata |
| FR-5–8 | Component tests kiểm tra tiêu đề, nhóm Bài, trạng thái và link học lại |
| FR-9–12 | Progress/lesson tests kiểm tra checkpoint và mở Ngày mới ngay |
| FR-13 | Progress regression test nhiều hoạt động cùng ngày chỉ tăng streak một lần |
| FR-14–15 | Component tests trạng thái generating/error/retry |
| FR-16–17 | Backend generation tests cùng cấp/tăng cấp |
| FR-18 | Service/component test trạng thái hoàn thành hành trình |

## Risks / Open Questions

- Tổng quan chứa toàn bộ Ngày có thể lớn sau thời gian dài; phân trang là hướng tối ưu sau MVP.
- Metadata Ngày phụ thuộc hồ sơ đồng bộ; client phải tải profile trước hoặc đồng bộ cùng phiên.
- Không có open question chặn triển khai.

## Related ADRs

- `docs/adr/2026-07-31-learning-day-container.md`
- `docs/adr/2026-07-31-server-owned-ai-paths.md`
