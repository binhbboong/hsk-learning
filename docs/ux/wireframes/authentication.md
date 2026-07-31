# Wireframe: Đăng ký và đăng nhập

## Purpose

Giúp người mới tạo hoặc mở đúng không gian học cá nhân với ít trở ngại nhất.

## Layout

```text
+------------------------------------------------------------------+
| Thương hiệu                                      Đã có tài khoản |
+--------------------------------+---------------------------------+
| Lời hứa ngắn                    | Đăng nhập / Đăng ký             |
| - Tiến độ riêng                 | - Tên (chỉ đăng ký)             |
| - Ôn đúng lúc                   | - Email                         |
| - Học tiếp trên thiết bị khác   | - Mật khẩu + hiện/ẩn            |
| Minh họa tiến trình             | [Hành động chính]               |
|                                 | Chuyển chế độ                   |
+--------------------------------+---------------------------------+
```

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Tiêu đề theo chế độ | Xác nhận người học đang đăng ký hay đăng nhập | 1 |
| Form và lỗi theo trường | Hoàn thành xác thực và sửa lỗi nhanh | 1 |
| Hiện/ẩn mật khẩu | Giảm lỗi nhập trên điện thoại | 2 |
| Lợi ích tài khoản | Giải thích vì sao cần đăng nhập | 2 |
| Chuyển đăng ký/đăng nhập | Cho phép sửa lựa chọn mà không quay lại | 2 |

## States

- Empty: form sạch, hành động chính rõ ràng.
- Loading: khóa nút gửi và hiển thị “Đang tạo tài khoản…” hoặc “Đang đăng nhập…”.
- Error: thông báo tổng quát có thể đọc bằng trình đọc màn hình và lỗi trường cụ thể.
- Populated: dữ liệu hợp lệ, mật khẩu vẫn che mặc định.
