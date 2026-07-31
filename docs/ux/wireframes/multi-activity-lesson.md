# Wireframe: Lesson player đa hoạt động
Supports journey: docs/ux/journeys/nguoi-moi-hoc-hsk-vong-hoc-hang-ngay.md

## Purpose

Đưa người học qua hội thoại, nghe, sắp xếp câu và phát âm trong một bài có tiến độ rõ ràng.

## Layout

```text
+--------------------------------------------------+
| Thoát | Bài n / hoạt động n | tiến độ             |
+--------------------------------------------------+
| Hội thoại: từng câu + [nghe câu]                  |
| [Pinyin bật/tắt] [Bản dịch bật/tắt]               |
| [Lưu từ]                                         |
+--------------------------------------------------+
| Hoạt động hiện tại                               |
| - nghe chọn đáp án / sắp xếp token / ghi âm      |
| - phản hồi và hành động tiếp                     |
+--------------------------------------------------+
```

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Audio từng câu | Gắn âm với ngữ cảnh | High |
| Toggle Pinyin/bản dịch | Điều chỉnh mức hỗ trợ | High |
| Activity progress | Giữ kỳ vọng về thời lượng | High |
| Listening/reorder/record controls | Luyện đủ kỹ năng | High |
| Save word | Nuôi sổ từ cá nhân | Medium |

## States

- Empty: bài không có hoạt động, quay về lộ trình.
- Loading: giữ header/progress và khung nội dung.
- Error: cho phép thử lại hoặc dùng transcript.
- Populated: một hoạt động mỗi bước, phản hồi trước khi tiếp tục.
- Completed: xác nhận hoàn thành Bài n và cho phép học ngay Bài n+1.
