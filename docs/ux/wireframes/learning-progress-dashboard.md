# Wireframe: Dashboard tiến độ
Supports journey: docs/ux/journeys/nguoi-moi-hoc-hsk-vong-hoc-hang-ngay.md

## Purpose

Cho người học biết nên học hay ôn gì tiếp theo và nhìn thấy nhịp học bền vững.

## Layout

```text
+--------------------------------------------------+
| HSK Learning | streak | tiến độ HSK 1             |
+--------------------------------------------------+
| Việc nên làm tiếp: [Tiếp tục bài / Làm checkpoint]|
+--------------------------------------------------+
| Bài đã hoàn thành | mục đến hạn | câu làm sai     |
+--------------------------------------------------+
| [Lộ trình bài] [Trung tâm ôn] [Sổ từ cá nhân]    |
+--------------------------------------------------+
```

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Hành động tiếp theo | Loại bỏ việc tự chọn mơ hồ | High |
| Streak | Khuyến khích quay lại hằng ngày | High |
| Tiến độ theo bài | Cho thấy vị trí trong lộ trình | High |
| Hàng đợi ôn/checkpoint | Báo nghĩa vụ học đúng lúc | High |
| Sổ từ | Truy cập bộ từ cá nhân | Medium |

## States

- Empty: chưa hoàn thành bài nào, đề xuất Bài 1.
- Loading: các chỉ số và CTA ở dạng khung.
- Error: dùng dữ liệu local cuối cùng và cảnh báo không tải được nội dung mới.
- Populated: streak, tiến độ, hàng đợi và CTA ưu tiên.
