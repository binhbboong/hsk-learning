# Specification: Tài khoản người học
Related UX: docs/ux/wireframes/authentication.md, docs/ux/wireframes/account-menu.md

## Status
Approved

## Overview

Mỗi người học cần một không gian riêng để tiến độ không bị trộn với người khác và có thể tiếp
tục sau khi đăng nhập lại. Trải nghiệm xác thực phải dễ hiểu với người mới, bằng tiếng Việt.

## User Scenarios

- Là người mới, tôi muốn đăng ký bằng tên, email và mật khẩu để bắt đầu lộ trình riêng.
- Là người học cũ, tôi muốn đăng nhập lại để tiếp tục đúng tiến độ.
- Là người dùng chung thiết bị, tôi muốn đăng xuất để người sau không thấy dữ liệu của tôi.

## Functional Requirements

- FR-1: Hệ thống MUST cho phép đăng ký bằng tên hiển thị, email hợp lệ và mật khẩu từ 8 ký tự.
- FR-2: Hệ thống MUST từ chối email đã tồn tại mà không tiết lộ mật khẩu hoặc dữ liệu nhạy cảm.
- FR-3: Hệ thống MUST cho phép đăng nhập bằng email và mật khẩu đúng.
- FR-4: Hệ thống MUST trả cùng một thông báo an toàn khi thông tin đăng nhập không hợp lệ.
- FR-5: Hệ thống MUST duy trì phiên sau khi tải lại trang và MUST cho phép đăng xuất.
- FR-6: Hệ thống MUST bảo vệ lộ trình học và chuyển khách tới đăng nhập.
- FR-7: Hệ thống MUST hiển thị tên và email của tài khoản đang hoạt động.
- FR-8: Hệ thống MUST lưu một hồ sơ học riêng cho từng tài khoản.
- FR-9: Hệ thống MUST không cho tài khoản A đọc hoặc sửa hồ sơ của tài khoản B.
- FR-10: Hệ thống MUST nhập hồ sơ ẩn danh hiện có khi tài khoản chưa có tiến độ.
- FR-11: Form MUST có trạng thái gửi, lỗi rõ ràng và điều khiển hiện/ẩn mật khẩu.
- FR-12: Phiên hết hạn MUST đưa người dùng về đăng nhập mà không làm rò dữ liệu tài khoản trước.

## Out of Scope

- Đăng nhập Google/Facebook/Apple.
- Xác minh email, quên hoặc đặt lại mật khẩu.
- Quản trị người dùng và phân quyền giáo viên.
- Ảnh đại diện tải lên.

## Open Questions

- Không có câu hỏi chặn; email + mật khẩu là phương thức đầu tiên.

## Acceptance Criteria

- [ ] Đăng ký thành công đưa người học vào `/learn`.
- [ ] Đăng nhập lại khôi phục đúng tiến độ, sổ từ và câu sai.
- [ ] Tài khoản khác trên cùng thiết bị thấy hồ sơ riêng.
- [ ] Khách mở `/learn` được chuyển tới đăng nhập rồi quay lại đúng trang.
- [ ] Đăng xuất xóa phiên phía khách và thu hồi phiên phía máy chủ.
- [ ] Giao diện xác thực dùng được ở 320px và bằng bàn phím.
