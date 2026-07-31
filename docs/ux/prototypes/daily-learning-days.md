# Prototype: Lộ trình học theo Ngày
Journey: docs/ux/journeys/nguoi-moi-hoc-hsk-vong-hoc-hang-ngay.md

## Screen Sequence

1. `docs/ux/wireframes/daily-learning-days.md` — mở trang học hoặc quay về từ một Bài.
2. `docs/ux/wireframes/multi-activity-lesson.md` — chọn hành động “Bắt đầu/Mở bài”.
3. `docs/ux/wireframes/continuous-lessons.md` — hoàn thành từng Bài.
4. `docs/ux/wireframes/checkpoint-test.md` — hoàn thành Bài thứ 5 của Ngày.
5. `docs/ux/wireframes/daily-learning-days.md` — checkpoint hoàn thành, AI tạo và mở Ngày kế tiếp.

## Transitions

| From | Trigger | To |
|---|---|---|
| Lộ trình theo Ngày | Chọn Bài chưa hoàn thành đầu tiên | Bài học đa hoạt động |
| Bài học | Hoàn thành Bài 1–4 trong Ngày | Xác nhận và Bài kế tiếp |
| Bài học | Hoàn thành Bài thứ 5 trong Ngày | Checkpoint đúng phạm vi |
| Checkpoint | Nộp câu cuối cùng | Lộ trình theo Ngày, trạng thái đang tạo |
| Đang tạo | AI tạo và lưu thành công | Ngày kế tiếp, Bài đầu tiên sẵn sàng |
| Đang tạo | AI hoặc kiểm định thất bại | Trạng thái lỗi và “Thử tạo lại” |

## Readiness for Specification

- [x] Mọi bước của journey có màn hình tương ứng.
- [x] Mọi chuyển trạng thái có trigger rõ ràng.
- [x] Không có màn hình ngoài nhu cầu của journey.
- [x] Không còn câu hỏi UX chặn triển khai.

## Open Questions

Không có. Ngày học là số thứ tự lộ trình, không phải ngày lịch.
