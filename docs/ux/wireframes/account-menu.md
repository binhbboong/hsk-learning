# Wireframe: Menu tài khoản

## Purpose

Cho người học luôn biết mình đang dùng tài khoản nào và có thể đăng xuất an toàn.

## Layout

```text
+---------------------------------------------------------------+
| HSK Learning      Học cho người Việt    [Tên người học ▾]     |
|                                           Email                |
|                                           Giao diện             |
|                                           [Hệ thống][Sáng][Tối] |
|                                           [Đăng xuất]          |
+---------------------------------------------------------------+
```

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Tên/ảnh chữ cái | Nhận biết tài khoản đang hoạt động | 1 |
| Email | Phân biệt tài khoản có tên giống nhau | 2 |
| Chế độ giao diện | Theo hệ thống thiết bị hoặc cho phép chọn Sáng/Tối và ghi nhớ lựa chọn | 2 |
| Đăng xuất | Kết thúc phiên và quay về đăng nhập | 1 |

## States

- Empty: khách được dẫn đến đăng nhập.
- Loading: khung tên trung tính, không nhấp nháy nội dung sai.
- Error: phiên hết hạn được xóa và chuyển về đăng nhập với lời giải thích.
- Populated: tên, email và nút đăng xuất hiển thị.
- Theme system: tự áp dụng và cập nhật khi thiết bị đổi chế độ sáng/tối.
- Theme override: lựa chọn Sáng hoặc Tối được lưu trên thiết bị và ưu tiên hơn cài đặt hệ thống.
