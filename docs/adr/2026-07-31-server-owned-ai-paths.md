# ADR: Server sở hữu và lưu bất biến lộ trình AI

Date: 2026-07-31
Slug: server-owned-ai-paths
Status: Accepted
Related spec: docs/specs/ai-daily-paths/Specification.md

## Context

Chặng AI phải ổn định khi tải lại, đồng bộ giữa thiết bị và không bị tạo trùng khi nhiều yêu
cầu cùng lúc. Lưu bundle trong hồ sơ client làm payload lớn, cho phép client ghi đè nội dung
và không tạo được ràng buộc idempotent đáng tin cậy. Tạo lại mỗi lần từ cùng prompt cũng
không đảm bảo nội dung giống nhau và làm tăng chi phí.

## Decision

Server sở hữu nội dung chặng AI và lưu mỗi bundle bất biến theo tài khoản cùng chỉ số chặng.
Chặng đã lưu được trả lại cho mọi yêu cầu lặp; chỉ bundle đầy đủ và qua kiểm định mới được
lưu. Hồ sơ học tiếp tục sở hữu tiến độ, SRS, lỗi sai, sổ từ và kết quả checkpoint.

## Consequences

- Nội dung ổn định và đồng bộ giữa thiết bị.
- Có thể bảo đảm idempotency bằng ràng buộc duy nhất ở tầng persistence.
- Server phải quản lý vòng đời và dung lượng của nội dung bài học đã tạo.
- API lộ trình cần xác thực tài khoản để đọc bài động.
- Việc xóa tài khoản phải xóa cả chặng AI liên quan.
