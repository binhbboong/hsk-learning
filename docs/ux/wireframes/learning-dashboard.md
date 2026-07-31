# Wireframe: Learning Dashboard

Supports journey: docs/ux/journeys/nguoi-moi-hoc-hsk-hoc-tu-vung-dau-tien.md

## Purpose

Cho người mới biết vị trí hiện tại và bắt đầu bài học phù hợp mà không phải tự cấu hình.

## Layout

```text
+------------------------------------------------------+
| Header: HSK Learning                     [Tiến độ]    |
+------------------------------------------------------+
| Main                                                  |
|  Chào mừng / lời hướng dẫn ngắn                       |
|  +------------------------------------------------+  |
|  | HSK 1 · Bài được đề xuất                       |  |
|  | Mục tiêu · số từ · thời lượng ước tính          |  |
|  | [Bắt đầu học]                                   |  |
|  +------------------------------------------------+  |
|  Lộ trình HSK 1–6: [1 hiện tại] [2..6 khóa/chưa học] |
|  Tổng quan: bài hoàn thành · từ đã học                |
+------------------------------------------------------+
```

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Bài được đề xuất | Giảm bối rối về bước tiếp theo | High |
| Bắt đầu học | Đưa người học vào phiên học | High |
| Lộ trình HSK 1–6 | Tạo bối cảnh và cảm giác tiến bộ | Medium |
| Tổng quan tiến độ | Củng cố động lực | Medium |

## States

- Empty: Giới thiệu HSK 1 và đề xuất bài đầu tiên.
- Loading: Giữ cấu trúc trang và báo đang chuẩn bị lộ trình.
- Error: Nêu không tải được dữ liệu và cho phép thử lại; vẫn giải thích điểm bắt đầu.
- Populated: Hiển thị bài tiếp theo, lộ trình và số liệu tiến độ.
