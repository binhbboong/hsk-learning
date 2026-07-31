# ADR: Tài khoản riêng và hồ sơ học trên máy chủ

Date: 2026-07-31
Slug: user-accounts
Status: Accepted
Related spec: docs/specs/user-accounts/Specification.md

## Context

HSK Learning đang lưu một hồ sơ ẩn danh trong `localStorage`. Cách này không tách được nhiều
người dùng trên cùng thiết bị, không hỗ trợ đăng nhập lại hoặc đồng bộ tiến độ, và mâu thuẫn
với yêu cầu mới về đăng ký/đăng nhập riêng từng người.

## Decision

Sản phẩm dùng tài khoản email + mật khẩu và tên hiển thị. FastAPI sở hữu danh tính, phiên đăng
nhập dạng bearer token thu hồi được, và hồ sơ học JSON riêng cho từng tài khoản trong SQLite.
Mật khẩu được băm bằng `scrypt` với salt riêng; token thô chỉ tồn tại ở phía khách, máy chủ chỉ
lưu hash. Angular bảo vệ khu vực `/learn`, lưu phiên hiện tại trong `localStorage`, tự gắn token
vào API, và nhập hồ sơ học ẩn danh hiện có vào tài khoản khi đăng nhập lần đầu.

## Consequences

- Tiến độ, streak, SRS, câu sai, sổ từ và checkpoint được tách theo người dùng.
- Đăng xuất không xóa dữ liệu học trên máy chủ; người khác đăng nhập không nhìn thấy dữ liệu đó.
- SQLite phù hợp bản local/MVP một máy chủ nhưng cần cơ sở dữ liệu quản lý khi triển khai
  serverless nhiều instance.
- Chưa có OAuth, xác minh email hay quên mật khẩu; các luồng này cần quyết định riêng.
- ADR `2026-07-30-persistent-learning-loop` bị thay thế.
