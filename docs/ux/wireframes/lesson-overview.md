# Wireframe: Lesson Overview

Supports journey: docs/ux/journeys/nguoi-moi-hoc-hsk-hoc-tu-vung-dau-tien.md

## Purpose

Giúp người học hiểu mục tiêu và quy mô phiên học trước khi bắt đầu.

## Layout

```text
+------------------------------------------------------+
| Header: [Về lộ trình]     HSK 1 · Bài từ vựng        |
+------------------------------------------------------+
| Main                                                  |
|  Tên bài                                              |
|  Mục tiêu học                                         |
|  5 từ · khoảng 5 phút                                 |
|  Nội dung hỗ trợ: pinyin · Hán–Việt · nghĩa · ví dụ  |
|                                                       |
|  [Bắt đầu flip-card]                                  |
+------------------------------------------------------+
```

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Mục tiêu bài | Đặt kỳ vọng rõ ràng | High |
| Quy mô và thời lượng | Giảm lo ngại phiên học quá dài | High |
| Phạm vi nội dung | Cho biết người học sẽ nhận được gì | Medium |
| Bắt đầu flip-card | Bắt đầu hành trình học | High |

## States

- Empty: Không có bài phù hợp; cho phép về lộ trình.
- Loading: Báo đang chuẩn bị nội dung bài học.
- Error: Báo không thể chuẩn bị bài và cho phép thử lại hoặc dùng bài mặc định.
- Populated: Hiển thị đầy đủ mục tiêu, quy mô và hành động bắt đầu.
