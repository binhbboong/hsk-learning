# Prototype: First Vocabulary Session

Journey: docs/ux/journeys/nguoi-moi-hoc-hsk-hoc-tu-vung-dau-tien.md

## Screen Sequence

1. `docs/ux/wireframes/learning-dashboard.md` — entry point khi người học mở ứng dụng.
2. `docs/ux/wireframes/lesson-overview.md` — triggered by chọn **Bắt đầu học** trên dashboard.
3. `docs/ux/wireframes/flip-card-study.md` — triggered by chọn **Bắt đầu flip-card**.
4. `docs/ux/wireframes/session-results.md` — triggered khi thẻ cuối đã được đánh giá.
5. `docs/ux/wireframes/flip-card-study.md` — optional, triggered by **Ôn lại từ chưa nhớ**.
6. `docs/ux/wireframes/learning-dashboard.md` — triggered by **Về lộ trình**.

## Transitions

| From | Trigger | To |
|---|---|---|
| Learning Dashboard | Chọn Bắt đầu học trên bài được đề xuất | Lesson Overview |
| Lesson Overview | Chọn Bắt đầu flip-card khi bài đã sẵn sàng | Flip-card Study |
| Flip-card Study | Chọn Lật thẻ | Flip-card Study, answer state |
| Flip-card Study | Chọn Đã nhớ hoặc Chưa nhớ; còn thẻ | Flip-card Study, next card |
| Flip-card Study | Chọn Đã nhớ hoặc Chưa nhớ; hết thẻ | Session Results |
| Session Results | Chọn Ôn lại từ chưa nhớ và có ít nhất một từ | Flip-card Study |
| Session Results | Chọn Về lộ trình | Learning Dashboard |

## Readiness for Specification

- [x] Every step of the source journey is covered by a screen in this flow.
- [x] Every transition has a clear, unambiguous trigger.
- [x] No screen exists in this flow without a stated purpose from the journey.
- [x] Open UX questions are listed below, not silently resolved.

## Open Questions

- MVP sẽ dùng một người học ẩn danh trên local; authentication được để ngoài specification
  đầu tiên và sẽ cần ADR riêng trước khi lưu dữ liệu đa người dùng.
- Cơ chế lập lịch ôn dài hạn sẽ được đặc tả sau MVP; phiên đầu chỉ hỗ trợ ôn lại các từ vừa
  đánh dấu Chưa nhớ.
- Nội dung AI không đạt yêu cầu hoặc thiếu API key sẽ rơi về bài học HSK 1 mặc định đã được
  kiểm soát, để luồng học vẫn hoàn tất.
