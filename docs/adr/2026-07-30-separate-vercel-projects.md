# ADR: Tách frontend và backend thành hai Vercel project

Date: 2026-07-30
Slug: separate-vercel-projects
Status: Accepted
Related spec: docs/specs/first-vocabulary-session/Specification.md

## Context

Angular và FastAPI cần cùng tồn tại trong một repository, chạy thuận tiện trên local và có
thể triển khai lên Vercel. Các lựa chọn gồm một Vercel project đa service, hai Vercel project
từ cùng monorepo, hoặc để FastAPI phục vụ cả static frontend. MVP ưu tiên cấu hình dễ hiểu,
khả năng build độc lập và tương thích với cách Vercel cấu hình root directory.

## Decision

Repository sẽ chứa `frontend/` và `backend/` như hai project độc lập. Mỗi thư mục là root
directory của một Vercel project. Frontend nhận base URL của API qua cấu hình build; backend
giới hạn CORS theo danh sách origin cấu hình qua môi trường.

Local development chạy Angular và FastAPI riêng, với Angular development server chuyển tiếp
đường dẫn `/api` tới FastAPI để giữ lời gọi cùng origin trong quá trình phát triển.

## Consequences

- Frontend và backend build, deploy và rollback độc lập.
- Cần cấu hình URL backend cho frontend production và origin frontend cho backend.
- Hai preview URL có thể thay đổi, nên cấu hình CORS phải hỗ trợ danh sách origin rõ ràng.
- Không phụ thuộc Vercel Services cho MVP.
- Có thể hợp nhất topology sau này bằng ADR mới nếu nhu cầu một domain hoặc atomic deploy trở
  nên quan trọng hơn.
