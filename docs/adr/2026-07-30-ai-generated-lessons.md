# ADR: Sử dụng AI API để tạo bài học phù hợp

Date: 2026-07-30
Slug: ai-generated-lessons
Status: Accepted
Related spec: Chưa có

## Context

HSK Learning hướng đến người Việt mới học tiếng Trung theo lộ trình HSK 1–6. Người học có
trình độ, tiến độ ghi nhớ và điểm yếu khác nhau ở từ vựng, ngữ pháp, nghe và phát âm, nên
một nội dung cố định khó luôn phù hợp với nhu cầu thực tế của từng người. Vision hiện tại
đã đặt mục tiêu cải thiện mức độ hoàn thành, khả năng ghi nhớ và kết quả kiểm tra nhưng chưa
ghi nhận cách AI sẽ hỗ trợ tạo nội dung phù hợp.

## Decision

HSK Learning sẽ tích hợp một dịch vụ AI thông qua API để hỗ trợ tạo bài học phù hợp với
trình độ và nhu cầu học tập của người dùng. API key phải được quản lý như thông tin bí mật ở
phía máy chủ, không được nhúng vào mã phía trình duyệt, ứng dụng khách hoặc kho mã nguồn.

Quyết định này chưa lựa chọn nhà cung cấp, mô hình AI, cấu trúc prompt hay cơ chế đánh giá
nội dung cụ thể; các lựa chọn đó sẽ được xác định trong PRD, Specification và
Implementation Plan.

## Consequences

- Bài học có thể thích ứng tốt hơn với trình độ, tiến độ và điểm yếu của người học.
- Sản phẩm cần có cơ chế kiểm soát chất lượng, độ chính xác và mức độ phù hợp của nội dung
  do AI tạo ra, đặc biệt với phát âm, ngữ pháp và phạm vi HSK.
- Hệ thống sẽ phát sinh chi phí API, độ trễ, giới hạn sử dụng và sự phụ thuộc vào dịch vụ
  bên ngoài.
- Dữ liệu gửi tới dịch vụ AI cần được tối thiểu hóa và xử lý theo yêu cầu về quyền riêng tư.
- Cần có phương án khi dịch vụ AI không khả dụng hoặc trả về nội dung không đạt yêu cầu.
