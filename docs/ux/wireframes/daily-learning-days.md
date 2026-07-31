# Wireframe: Lộ trình học theo Ngày
Supports journey: docs/ux/journeys/nguoi-moi-hoc-hsk-vong-hoc-hang-ngay.md

## Purpose

Cho người học biết đang ở Ngày nào, còn bao nhiêu Bài và cách mở Ngày kế tiếp.

## Layout

```text
+------------------------------------------------------+
| Lộ trình HSK 1                         Chuỗi 3 ngày   |
| Học theo từng Ngày, tiến bộ qua từng Bài.            |
+------------------------------------------------------+
| VIỆC NÊN LÀM TIẾP                                    |
| Tiếp tục Bài 7                              [Bắt đầu] |
+------------------------------------------------------+
| 5/10 Bài | 0 thẻ đến hạn | 1 câu cần sửa            |
+------------------------------------------------------+
| NGÀY 2 · ĐANG HỌC · HSK 1 · ĐỘ KHÓ 2/5              |
| Tiến độ 1/5                                          |
| 06 Bài ...                                  [Học lại]|
| 07 Bài ...                                  [Mở bài] |
| 08 Bài ...                                  [Mở bài] |
| 09 Bài ...                                  [Mở bài] |
| 10 Bài ...                                  [Mở bài] |
| Checkpoint Bài 6–10                         [Đã khóa] |
+------------------------------------------------------+
| NGÀY 1 · HOÀN THÀNH                                  |
| Bài 1–5 · Checkpoint 3/3                    [Xem lại] |
+------------------------------------------------------+
| Ôn flipcard | Ôn câu sai | Sổ từ                     |
+------------------------------------------------------+
```

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Ngày hiện tại | Tạo mốc tiến độ dễ hiểu | High |
| Hành động tiếp theo | Đưa người học vào đúng Bài/checkpoint | High |
| Tiến độ 5 Bài của Ngày | Cho biết còn bao nhiêu Bài trước checkpoint | High |
| Trạng thái Ngày | Phân biệt đang học và hoàn thành | High |
| Cấp HSK và độ khó | Giải thích vì sao nội dung thay đổi | Medium |
| Checkpoint của Ngày | Làm rõ điều kiện mở Ngày kế tiếp | Medium |
| Ngày cũ | Cho phép xem và học lại | Medium |

## States

- Empty: Ngày 1 hiển thị 0/5 Bài và Bài 1 là hành động chính.
- Loading: giữ khung Ngày hiện tại và thông báo đang tải lộ trình.
- Generating: hiển thị “AI đang chuẩn bị Ngày N+1” và vô hiệu hóa yêu cầu lặp.
- Error: giữ nguyên Ngày vừa hoàn thành, giải thích lỗi và có nút “Thử tạo lại”.
- Populated: Ngày hiện tại mở rộng; các Ngày hoàn thành vẫn hiển thị để xem lại.
- Journey complete: hiển thị đã hoàn thành HSK 1–6, không tạo Ngày mới.
