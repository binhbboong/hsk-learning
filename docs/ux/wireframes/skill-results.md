# Wireframe: Kết quả kỹ năng
Supports journey: docs/ux/journeys/nguoi-moi-hoc-hsk-luyen-da-ky-nang.md

## Purpose

Tóm tắt kết quả bài vừa học và chỉ rõ bài nên học tiếp theo.

## Layout

```text
+--------------------------------------------------+
| Hoàn thành bài                                   |
| Tên kỹ năng + điểm / mức tự đánh giá             |
+--------------------------------------------------+
| Điều đã làm tốt                                  |
| Điều cần luyện lại                               |
+--------------------------------------------------+
| [Học lại] [Chọn kỹ năng khác]                    |
+--------------------------------------------------+
```

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Kết quả | Tạo bằng chứng hoàn thành | High |
| Nhận xét | Biến kết quả thành hành động | High |
| Hành động tiếp theo | Giữ nhịp học | High |

## States

- Empty: chưa có kết quả, quay về danh mục.
- Loading: không áp dụng vì kết quả tính trong phiên.
- Error: giữ kết quả cơ bản nếu nhận xét chi tiết không tải được.
- Populated: điểm, nhận xét và hai hành động tiếp theo.
