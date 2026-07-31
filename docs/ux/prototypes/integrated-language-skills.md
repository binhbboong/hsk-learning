# Prototype: Luyện đa kỹ năng HSK 1
Journey: docs/ux/journeys/nguoi-moi-hoc-hsk-luyen-da-ky-nang.md

## Screen Sequence

1. `docs/ux/wireframes/skills-catalog.md` — vào từ trang chủ.
2. `docs/ux/wireframes/grammar-practice.md` — chọn Ngữ pháp.
3. `docs/ux/wireframes/listening-practice.md` — chọn Nghe hiểu.
4. `docs/ux/wireframes/pronunciation-coach.md` — chọn Phát âm.
5. `docs/ux/wireframes/skill-results.md` — hoàn thành bài đã chọn.

Mỗi bài kỹ năng là một nhánh độc lập từ danh mục tới kết quả; người học không bắt buộc hoàn
thành cả ba trong cùng phiên.

## Transitions

| From | Trigger | To |
|---|---|---|
| Danh mục | Chọn thẻ Ngữ pháp | Bài ngữ pháp |
| Danh mục | Chọn thẻ Nghe hiểu | Bài nghe |
| Danh mục | Chọn thẻ Phát âm | Phòng luyện phát âm |
| Bài ngữ pháp | Trả lời câu cuối | Kết quả kỹ năng |
| Bài nghe | Gửi đáp án | Kết quả kỹ năng |
| Phòng phát âm | Hoàn tất tự đánh giá | Kết quả kỹ năng |
| Kết quả | Chọn kỹ năng khác | Danh mục |
| Kết quả | Học lại | Bài vừa hoàn thành |

## Readiness for Specification

- [x] Every step of the source journey is covered by a screen in this flow.
- [x] Every transition has a clear, unambiguous trigger.
- [x] No screen exists in this flow without a stated purpose from the journey.
- [x] Open UX questions are listed below, not silently resolved.

## Open Questions

- Phân tích âm thanh tự động bằng AI được để sau vòng ghi âm/playback đầu tiên; MVP vẫn phải
  đưa phản hồi thanh điệu cụ thể theo mẫu và cho người học tự đánh giá.
