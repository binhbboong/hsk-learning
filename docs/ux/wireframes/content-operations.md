# Wireframe: Quản trị nội dung AI

## Purpose

Cho người vận hành xem chất lượng, chi phí, sửa và quyết định phát hành nội dung AI.

## Layout

```text
+------------------------------------------------------+
| Header: Quản trị nội dung | Hôm nay: lượt / giới hạn |
+------------------------------------------------------+
| Bộ lọc: Chờ duyệt | Đã duyệt | Từ chối               |
+----------------------+-------------------------------+
| Danh sách nội dung   | Chi tiết Ngày                |
| Ngày · HSK · trạng   | Kiểm tra chất lượng          |
| thái · chủ tài khoản | 5 Bài + checkpoint           |
|                      | Trình sửa JSON có cấu trúc    |
|                      | [Lưu] [Duyệt] [Từ chối]       |
+----------------------+-------------------------------+
```

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Tổng quan quota/usage | Kiểm soát vận hành và chi phí | 1 |
| Hàng đợi chờ duyệt | Tập trung nội dung chưa phát hành | 1 |
| Báo cáo kiểm tra chất lượng | Nêu lỗi phạm vi, thiếu dữ liệu, trùng lặp | 1 |
| Trình sửa nội dung | Sửa trước khi duyệt | 2 |
| Nhật ký quyết định | Biết ai duyệt/từ chối và khi nào | 2 |

## States

- Empty: không có nội dung chờ duyệt; vẫn hiển thị usage.
- Loading: khóa hành động quyết định và giữ danh sách khung.
- Error: báo lỗi tải/lưu cụ thể, không làm mất bản sửa đang nhập.
- Populated: chọn một mục, xem kiểm tra chất lượng, sửa, duyệt hoặc từ chối.

