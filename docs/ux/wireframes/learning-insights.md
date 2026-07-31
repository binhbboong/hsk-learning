# Wireframe: Phân tích tiến độ học
Supports journey: docs/ux/journeys/nguoi-moi-hoc-hsk-vong-hoc-hang-ngay.md

## Purpose

Giúp người mới biết mức độ đều đặn, kỹ năng yếu và hành động ôn tập tốt nhất tiếp theo.

## Layout

```text
+------------------------------------------------------+
| Header: HSK hiện tại · chuỗi ngày                     |
+------------------------------------------------------+
| Việc nên làm tiếp                                    |
| [Bắt đầu bài / Ôn điểm yếu]                          |
+------------------------------------------------------+
| 7 ngày hoạt động        | 30 ngày ghi nhớ            |
| [7 ô ngày]              | tỷ lệ nhớ · xu hướng       |
+------------------------------------------------------+
| Kỹ năng cần ưu tiên                                  |
| Nghe | Sắp xếp câu | Từ vựng | Phát âm              |
| [mức độ + lý do] [Ôn ngay]                           |
+------------------------------------------------------+
| Lộ trình các Ngày hiện có                            |
+------------------------------------------------------+
```

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Gợi ý ôn cá nhân hóa | Chuyển dữ liệu thành hành động cụ thể | 1 |
| Hoạt động 7 ngày | Cho thấy tính đều đặn gần đây | 2 |
| Ghi nhớ 30 ngày | Theo dõi mục tiêu ghi nhớ dài hạn | 2 |
| Điểm yếu theo kỹ năng | Giải thích vì sao hệ thống đề xuất ôn | 2 |
| Lộ trình Ngày | Giữ luồng học chính hiện có | 3 |

## States

- Empty: giải thích rằng dữ liệu sẽ xuất hiện sau bài học đầu tiên; vẫn mở Bài 1 HSK 1.
- Loading: khung chỉ báo đang tải, không che hành động học tiếp.
- Error: giữ lộ trình học và báo riêng rằng phân tích tạm thời chưa có.
- Populated: hiển thị 7 ngày, 30 ngày, kỹ năng yếu và một hành động ôn ưu tiên.

