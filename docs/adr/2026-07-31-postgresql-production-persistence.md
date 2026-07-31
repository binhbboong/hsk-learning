# ADR: Dùng PostgreSQL cho persistence production

Date: 2026-07-31
Slug: postgresql-production-persistence
Status: Accepted
Related spec: docs/specs/user-accounts/Specification.md

## Context

HSK Learning lưu tài khoản, phiên đăng nhập, hồ sơ học, lộ trình AI, draft nội dung và usage
trong SQLite. Cách này phù hợp local và test nhưng filesystem của Vercel Functions không phải
kho dữ liệu bền vững; database trong `/tmp` có thể biến mất khi instance được thay thế. Sản phẩm
cần giữ tài khoản và tiến độ qua các lần deploy và cold start.

## Decision

Production dùng PostgreSQL serverless được cấp qua Vercel Marketplace và kết nối bằng
`DATABASE_URL`. Repository duy trì cùng một hợp đồng nghiệp vụ cho PostgreSQL và SQLite:
PostgreSQL là lựa chọn khi có `DATABASE_URL`, còn SQLite tiếp tục là mặc định cho local và test.

Schema được khởi tạo idempotent khi ứng dụng khởi động. Kết nối PostgreSQL dùng driver Psycopg,
TLS/connection string do nhà cung cấp quản lý, và transaction ngắn theo từng thao tác repository.
Không ghi connection string vào source hoặc log.

## Consequences

- Tài khoản, session, tiến độ, daily path, content draft và AI usage tồn tại bền vững trên Vercel.
- Local development và test hiện tại không bắt buộc chạy PostgreSQL.
- Backend có thêm dependency `psycopg[binary]` và phải kiểm thử cả hai dialect.
- Deployment cần provision PostgreSQL, inject `DATABASE_URL`, đặt database gần Vercel Functions
  và theo dõi giới hạn connection của môi trường serverless.
- Quyết định này thay thế phần lựa chọn SQLite cho production trong ADR user-accounts; các phần
  về mô hình tài khoản, session và profile của ADR đó vẫn còn hiệu lực.
