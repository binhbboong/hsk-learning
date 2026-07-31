# ADR: Sử dụng FastAPI, Angular và Vercel

Date: 2026-07-30
Slug: fastapi-angular-vercel
Status: Accepted
Related spec: Chưa có

## Context

HSK Learning cần một website chạy được trên máy local và có thể triển khai lên Vercel.
Sản phẩm gồm trải nghiệm học tương tác trên trình duyệt, API phục vụ nội dung và tiến độ học,
và tích hợp dịch vụ AI bằng thông tin xác thực được bảo vệ phía máy chủ.

## Decision

Frontend của HSK Learning sẽ sử dụng Angular, backend API sử dụng FastAPI và mục tiêu triển
khai là Vercel. Cấu trúc triển khai phải giữ API key và các bí mật ở phía máy chủ, hỗ trợ
chạy toàn bộ hệ thống trên local và cho phép frontend gọi API qua cấu hình môi trường.

Các chi tiết về phiên bản framework, thư viện lưu trữ và cấu trúc triển khai cụ thể sẽ được
xác định trong Implementation Plan dựa trên khả năng tương thích đã kiểm chứng.

## Consequences

- Frontend và backend có ranh giới rõ ràng, có thể phát triển và kiểm thử độc lập.
- Local development cần quy trình chạy đồng thời Angular và FastAPI cùng cấu hình CORS phù hợp.
- Vercel cần cấu hình build frontend và định tuyến backend Python tương thích với nền tảng.
- Các giới hạn runtime, thời gian thực thi và lưu trữ của Vercel phải được tính đến, nhất là
  với việc tạo bài học bằng AI.
- Cần kiểm chứng deployment bằng build thực tế và tài liệu nền tảng hiện hành trước khi tuyên
  bố sẵn sàng triển khai.
