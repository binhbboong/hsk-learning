# Prototype: Học thích nghi và vận hành nội dung
Journey: docs/ux/journeys/nguoi-moi-hoc-hsk-vong-hoc-hang-ngay.md

## Screen Sequence

1. `docs/ux/wireframes/learning-insights.md` — sau đăng nhập hoặc quay về lộ trình.
2. Bài học phát âm hiện có — khi người học mở hoạt động phát âm và gửi bản thu.
3. Trung tâm ôn tập hiện có — khi người học chọn đề xuất ôn điểm yếu.
4. `docs/ux/wireframes/content-operations.md` — khi tài khoản quản trị mở khu vực quản trị.

## Transitions

| From | Trigger | To |
|---|---|---|
| Phân tích tiến độ | Chọn “Ôn ngay” | Trung tâm ôn tập với nguồn phù hợp |
| Phân tích tiến độ | Chọn Bài tiếp theo | Bài học đang mở |
| Bài học phát âm | Dừng thu và chọn phân tích | Phản hồi âm tiết/thanh điệu trong cùng bài |
| Quản trị nội dung | Chọn mục chờ duyệt | Chi tiết nội dung trong cùng màn |
| Chi tiết nội dung | Lưu bản sửa hợp lệ | Chi tiết đã cập nhật |
| Chi tiết nội dung | Duyệt | Nội dung được phát hành và chuyển sang Đã duyệt |
| Chi tiết nội dung | Từ chối | Nội dung không phát hành và chuyển sang Từ chối |

## Readiness for Specification

- [x] Mỗi bước của hành trình học có màn hình hoặc trạng thái tương ứng.
- [x] Mỗi chuyển tiếp có trigger rõ ràng.
- [x] Không có màn hình ngoài nhu cầu học hoặc vận hành đã nêu.
- [x] Không còn câu hỏi UX mở.

## Open Questions

- Không có.

