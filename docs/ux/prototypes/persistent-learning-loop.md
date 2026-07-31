# Prototype: Vòng học bền vững HSK 1
Journey: docs/ux/journeys/nguoi-moi-hoc-hsk-vong-hoc-hang-ngay.md

## Screen Sequence

1. `learning-progress-dashboard.md` — mở ứng dụng.
2. `multi-activity-lesson.md` — tiếp tục bài được đề xuất.
3. `review-center.md` — có thẻ đến hạn hoặc chọn ôn sai.
4. `checkpoint-test.md` — tự động mở sau mỗi nhóm 5 bài.
5. `personal-vocabulary.md` — mở từ dashboard hoặc thao tác lưu từ.

## Transitions

| From | Trigger | To |
|---|---|---|
| Dashboard | Chọn tiếp tục bài | Lesson player |
| Lesson player | Hoàn thành mọi hoạt động | Dashboard hoặc Checkpoint |
| Dashboard | Chọn mục đến hạn/câu sai | Review center |
| Review center | Hoàn thành hàng đợi | Dashboard |
| Dashboard | Checkpoint đang mở khóa | Checkpoint |
| Checkpoint | Gửi câu cuối | Kết quả checkpoint |
| Kết quả checkpoint | Chọn ôn sai | Review center |
| Dashboard | Mở sổ từ | Personal vocabulary |
| Personal vocabulary | Chọn ôn các từ | Review center |

## Readiness for Specification

- [x] Every step of the source journey is covered by a screen in this flow.
- [x] Every transition has a clear, unambiguous trigger.
- [x] No screen exists in this flow without a stated purpose from the journey.
- [x] Open UX questions are listed below, not silently resolved.

## Open Questions

- Cập nhật 2026-07-31: luồng tài khoản và đồng bộ hồ sơ được định nghĩa tại
  `docs/specs/user-accounts/Specification.md`; giả định ẩn danh ban đầu đã bị thay thế.
- Không có câu hỏi chặn. Phiên bản ẩn danh lưu trên một thiết bị; đồng bộ tài khoản nằm ngoài
  phạm vi.
