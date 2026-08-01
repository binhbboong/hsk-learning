# ADR: Server sở hữu nội dung phiên từ vựng theo chủ đề

Date: 2026-08-01
Slug: server-owned-topic-vocabulary
Status: Accepted
Related spec: `docs/specs/topic-vocabulary-learning/Specification.md`

## Context

Phiên từ vựng do AI tạo phải giữ nguyên khi tải lại, đồng bộ giữa thiết bị, chỉ chứa nội dung đã kiểm
định và không bị client ghi đè. Tuy nhiên trạng thái đang xem thẻ, kết quả nhớ từ, SRS và streak là dữ
liệu học tập của người dùng, cần đi cùng learning profile hiện có.

## Decision

Server sở hữu và lưu bất biến danh sách đề xuất gần nhất cùng bundle 10 từ theo tài khoản. Client chỉ
được yêu cầu danh sách, refresh và bắt đầu/tiếp tục phiên; không được gửi ngược nội dung chuẩn để lưu.
Learning profile tiếp tục sở hữu tiến độ theo chủ đề, vị trí phiên, kết quả, SRS và activity streak.
Mọi từ dùng ID chuẩn hóa để dùng chung trạng thái với lịch ôn và sổ từ. Khi AI không khả dụng hoặc nội
dung không vượt kiểm định, server trả bộ chủ đề/từ dự phòng đã kiểm duyệt.

## Consequences

- Nội dung phiên ổn định, đồng bộ và không phát sinh chi phí AI khi tải lại.
- Có thể chống tạo trùng bằng ràng buộc persistence ở phía server.
- Profile vẫn nhỏ vì chỉ chứa tiến độ và định danh, không chứa toàn bộ nội dung AI.
- Cần quản lý hai loại dữ liệu và xóa cả bundle khi xóa tài khoản.
- Danh mục dự phòng cần được duy trì và kiểm thử đủ 10 từ duy nhất theo phạm vi hỗ trợ.
