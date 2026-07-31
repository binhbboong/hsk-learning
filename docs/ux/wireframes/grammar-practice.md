# Wireframe: Bài ngữ pháp tương tác
Supports journey: docs/ux/journeys/nguoi-moi-hoc-hsk-luyen-da-ky-nang.md

## Purpose

Giải thích một mẫu câu HSK bằng tiếng Việt rồi cho người học áp dụng ngay.

## Layout

```text
+--------------------------------------------------+
| Thoát | Ngữ pháp HSK 1 | tiến độ câu hỏi          |
+--------------------------------------------------+
| Mẫu câu chính                                    |
| Ý nghĩa + giải thích cho người Việt              |
| Ví dụ chữ Hán / pinyin / tiếng Việt              |
+--------------------------------------------------+
| Câu hỏi lựa chọn hoặc sắp xếp câu                 |
| [các đáp án]                                     |
| [Kiểm tra]                                       |
+--------------------------------------------------+
| Phản hồi đúng/sai + giải thích + [Tiếp tục]       |
+--------------------------------------------------+
```

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Mẫu câu và giải thích | Tạo mô hình tinh thần trước khi làm bài | High |
| Câu hỏi | Kiểm tra khả năng vận dụng | High |
| Phản hồi tức thời | Sửa hiểu nhầm bằng tiếng Việt | High |
| Tiến độ | Giảm cảm giác bài học kéo dài | Medium |

## States

- Empty: không có câu hỏi, quay về danh mục.
- Loading: khung mẫu câu và câu hỏi.
- Error: thông báo và thử tải lại.
- Populated: mẫu câu, một câu hỏi mỗi bước và phản hồi sau khi trả lời.
