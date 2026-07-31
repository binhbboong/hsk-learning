# Implementation Plan: Tài khoản người học
Spec: docs/specs/user-accounts/Specification.md

## Approach

Ba hướng được cân nhắc: dịch vụ Auth bên ngoài, JWT tự chứa, hoặc phiên token thu hồi được trong
SQLite. Chọn phiên token + SQLite vì không thêm nhà cung cấp, dễ cô lập dữ liệu và đăng xuất có
hiệu lực ngay. Đổi lại, triển khai nhiều instance sau này cần chuyển SQLite sang database quản lý.

## File/Module Structure

| Path | Responsibility | Implements |
|---|---|---|
| backend/hsk_api/auth/* | Băm mật khẩu, token và xác thực request | FR-1–FR-5 |
| backend/hsk_api/repositories/accounts.py | Lưu tài khoản, phiên và hồ sơ riêng | FR-2, FR-8, FR-9 |
| backend/hsk_api/routers/auth.py | Register, login, me, logout | FR-1–FR-7 |
| backend/hsk_api/routers/profile.py | Đọc/ghi hồ sơ người học hiện tại | FR-8–FR-10 |
| frontend/src/app/core/auth/* | Phiên, interceptor và guard | FR-5, FR-6, FR-12 |
| frontend/src/app/features/auth/* | Form xác thực | authentication.md |
| frontend/src/app/app.* | Menu tài khoản toàn cục | account-menu.md |
| frontend/src/app/core/services/learning-profile.repository.ts | Đồng bộ hồ sơ local/server | FR-8–FR-10 |

## Testing Strategy

| Requirement | Verified by |
|---|---|
| FR-1–FR-5 | API tests đăng ký, đăng nhập, phiên và đăng xuất |
| FR-6–FR-7, FR-11–FR-12 | Angular guard/auth component tests |
| FR-8–FR-10 | API isolation tests và repository sync tests |
| Acceptance criteria | Playwright với hai tài khoản |

## Risks / Open Questions

- SQLite local không phù hợp Vercel filesystem tạm; production cần Postgres hoặc dịch vụ auth.
- Hồ sơ JSON dùng optimistic last-write-wins trong MVP.

## Related ADRs

- docs/adr/2026-07-31-user-accounts.md
