# Wireframe: Sổ từ cá nhân
Supports journey: docs/ux/journeys/nguoi-moi-hoc-hsk-vong-hoc-hang-ngay.md

## Purpose

Cho người học quản lý và bắt đầu ôn những từ tự chọn trong các bài.

## Layout

```text
+--------------------------------------------------+
| Sổ từ của tôi | số từ                            |
+--------------------------------------------------+
| Tìm kiếm / lọc đến hạn                           |
| chữ Hán | pinyin | nghĩa | nguồn bài | [Xóa]     |
+--------------------------------------------------+
| [Ôn các từ này]                                  |
+--------------------------------------------------+
```

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Danh sách từ | Nhìn lại nội dung tự chọn | High |
| Nguồn bài | Giữ ngữ cảnh | Medium |
| Xóa | Cho người học kiểm soát bộ từ | Medium |
| Bắt đầu ôn | Biến danh sách thành hành động | High |

## States

- Empty: giải thích cách lưu từ trong lesson.
- Loading: đọc dữ liệu local.
- Error: cảnh báo dữ liệu hỏng và không xóa im lặng.
- Populated: danh sách có thể tìm, xóa và ôn.
