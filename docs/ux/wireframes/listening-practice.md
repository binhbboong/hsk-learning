# Wireframe: Bài nghe hiểu
Supports journey: docs/ux/journeys/nguoi-moi-hoc-hsk-luyen-da-ky-nang.md

## Purpose

Cho người học nghe câu HSK 1 trước khi nhìn transcript và kiểm tra ý nghĩa nghe được.

## Layout

```text
+--------------------------------------------------+
| Thoát | Nghe HSK 1 | lượt nghe                    |
+--------------------------------------------------+
| Hướng dẫn: nghe trước, chưa xem chữ               |
| [Phát tốc độ thường] [Phát chậm]                  |
| [Hiện transcript]                                 |
+--------------------------------------------------+
| Câu hỏi nghe hiểu                                 |
| [đáp án A] [đáp án B] [đáp án C]                 |
+--------------------------------------------------+
| Phản hồi + transcript chữ Hán/pinyin/tiếng Việt   |
+--------------------------------------------------+
```

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Điều khiển audio | Cho phép nghe thường hoặc chậm | High |
| Transcript có kiểm soát | Ngăn người học đọc thay vì nghe | High |
| Câu hỏi nghe hiểu | Đo nhận biết ý nghĩa | High |
| Phản hồi | Kết nối âm thanh với chữ và nghĩa | High |

## States

- Empty: không có đoạn nghe và quay về danh mục.
- Loading: vùng audio/câu hỏi ở trạng thái chờ.
- Error: cho phép đọc transcript và học tiếp nếu audio không khả dụng.
- Populated: audio, transcript ẩn, câu hỏi và phản hồi.
