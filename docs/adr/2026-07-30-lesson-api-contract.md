# ADR: Dùng hợp đồng lesson API có cấu trúc

Date: 2026-07-30
Slug: lesson-api-contract
Status: Accepted
Related spec: docs/specs/first-vocabulary-session/Specification.md

## Context

Angular cần nhận một bài học hoàn chỉnh từ FastAPI dù nội dung đến từ dữ liệu mặc định hay
AI. Nếu client phải hiểu từng nhà cung cấp hoặc nhiều hình dạng dữ liệu, logic fallback và
kiểm soát chất lượng sẽ bị phân tán.

## Decision

FastAPI sẽ cung cấp một hợp đồng HTTP phiên bản hóa cho bài học đề xuất. Backend chịu trách
nhiệm tạo hoặc lấy bài, kiểm tra schema và trả cùng một cấu trúc lesson/card cho frontend.
Response kèm `source` để phân biệt nội dung `ai` và `fallback`, nhưng không chứa secret hoặc
chi tiết xác thực nhà cung cấp.

MVP dùng endpoint đọc bài đề xuất và không lưu rating trên backend; trạng thái phiên học nằm
ở frontend trong browser session.

## Consequences

- Frontend không phụ thuộc vào SDK hoặc schema của nhà cung cấp AI.
- Fallback và AI có thể được kiểm thử bằng cùng contract.
- Thay đổi phá vỡ contract cần version mới hoặc migration có chủ đích.
- Tiến độ chưa đồng bộ qua thiết bị trong MVP.
