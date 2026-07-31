# ADR: Dùng vòng học bền vững trên thiết bị cho người dùng ẩn danh

Date: 2026-07-30
Slug: persistent-learning-loop
Status: Superseded by 2026-07-31-user-accounts
Related spec: docs/specs/persistent-learning-loop/Specification.md

## Context

MVP hiện chỉ giữ kết quả trong `sessionStorage`, nên người học mất tiến độ khi đóng phiên và
không thể có ôn tập ngắt quãng, chuỗi ngày học, kiểm tra định kỳ, sổ từ hay danh sách lỗi
sai. Người dùng mục tiêu vẫn chưa cần tài khoản và sản phẩm chưa có cơ sở dữ liệu dài hạn.

## Decision

HSK Learning sẽ lưu trạng thái học ẩn danh bền vững trên chính thiết bị cho phiên bản đầu:
tiến độ theo bài, lịch SRS, streak, sổ từ cá nhân, câu làm sai và kết quả kiểm tra. Mỗi năm
bài hoàn thành mở một bài kiểm tra checkpoint. Audio ghi âm vẫn chỉ tồn tại tạm thời và
không được lưu cùng hồ sơ học.

## Consequences

- Người học có thể tiếp tục sau khi đóng/mở trình duyệt và nhận đúng nội dung cần ôn.
- Không cần tài khoản hoặc backend database trong giai đoạn này.
- Dữ liệu không đồng bộ giữa thiết bị và có thể mất khi xóa dữ liệu trình duyệt.
- Schema lưu trữ phải có version và xử lý dữ liệu hỏng an toàn.
- Khi thêm tài khoản sau này cần migration từ hồ sơ local sang hồ sơ máy chủ.
