# Specification: Học thích nghi và vận hành nội dung
Related UX: docs/ux/prototypes/learning-intelligence-operations.md

## Status

Approved

## Overview

Mở rộng HSK Learning bằng bốn năng lực: kiểm soát chất lượng và chi phí nội dung AI, phản hồi
phát âm theo âm tiết/thanh điệu cho người Việt, phân tích tiến độ 7/30 ngày với gợi ý ôn cá nhân
hóa, và công cụ quản trị nội dung trước khi phát hành. Người học mới có thể bắt đầu HSK 1 ngay hoặc
dùng bài kiểm tra đầu vào tùy chọn được đặc tả riêng tại `hsk-placement-test`.

## User Scenarios

- Là người mới, tôi muốn có thể bỏ qua kiểm tra và vào thẳng Bài 1 HSK 1.
- Là người học, tôi muốn biết âm tiết hoặc thanh điệu cần luyện và nhận mẹo bằng tiếng Việt.
- Là người học, tôi muốn thấy hoạt động 7 ngày, ghi nhớ 30 ngày và kỹ năng yếu để biết nên ôn gì.
- Là người vận hành, tôi muốn biết nội dung AI có trùng, vượt HSK hoặc thiếu thành phần hay không.
- Là người vận hành, tôi muốn giới hạn lượt tạo và xem usage để kiểm soát chi phí.
- Là quản trị viên, tôi muốn sửa, duyệt hoặc từ chối nội dung AI trước khi phát hành thủ công.

## Functional Requirements

- FR-1: Tài khoản mới MUST có lựa chọn bắt đầu HSK 1 ngay; bài kiểm tra đầu vào MUST NOT là bắt buộc.
- FR-2: Nội dung AI MUST được kiểm tra đủ 5 Bài, checkpoint, đúng cấp HSK và đầy đủ hoạt động.
- FR-3: Nội dung AI MUST bị đánh dấu khi mục tiêu hoặc từ vựng trùng quá ngưỡng với nội dung gần đây.
- FR-4: Nội dung không đạt kiểm tra MUST NOT được phát hành cho người học.
- FR-5: Hệ thống MUST áp dụng giới hạn tạo nội dung theo tài khoản và toàn hệ thống trong ngày.
- FR-6: Hệ thống MUST ghi số lượt, trạng thái, thời điểm và lượng token usage khi nhà cung cấp trả về.
- FR-7: Quản trị viên MUST xem được usage hiện tại và danh sách nội dung theo trạng thái.
- FR-8: Chỉ tài khoản được cấu hình là quản trị viên MUST truy cập được chức năng quản trị.
- FR-9: Quản trị viên MUST xem, sửa một bản nháp hợp lệ, duyệt hoặc từ chối nội dung.
- FR-10: Nội dung chờ duyệt hoặc bị từ chối MUST NOT xuất hiện trong lộ trình người học.
- FR-11: Phân tích phát âm MUST trả điểm nội dung, điểm tổng thể và quan sát cho từng âm tiết.
- FR-12: Mỗi quan sát âm tiết MUST nêu pinyin mục tiêu, thanh điệu mục tiêu, trạng thái và mẹo sửa tiếng Việt.
- FR-13: Phản hồi phát âm MUST nêu rõ đây là hỗ trợ luyện tập, không phải điểm thi hay giáo viên.
- FR-14: Hồ sơ MUST ghi hoạt động học theo ngày và loại hoạt động.
- FR-15: Dashboard MUST hiển thị trạng thái hoạt động trong 7 ngày gần nhất.
- FR-16: Dashboard MUST hiển thị tỷ lệ ghi nhớ từ vựng 30 ngày hoặc trạng thái chưa đủ dữ liệu.
- FR-17: Dashboard MUST xếp hạng điểm yếu từ nghe, sắp xếp câu, từ vựng và phát âm dựa trên bằng chứng đã lưu.
- FR-18: Dashboard MUST đưa ra đúng một gợi ý ôn ưu tiên với lý do và liên kết hành động.
- FR-19: Khi dữ liệu phân tích thiếu hoặc lỗi, người học MUST vẫn mở được Bài tiếp theo.
- FR-20: Sau điểm bắt đầu tùy chọn, hệ thống MUST tiếp tục điều chỉnh cấp/độ khó từ kết quả trong quá trình học.

## Out of Scope

- Chi tiết chấm và giao diện bài đầu vào (thuộc đặc tả `hsk-placement-test`).
- Cam kết chấm thanh điệu chính xác tương đương giáo viên.
- Thanh toán, hóa đơn hoặc tự động mua thêm quota OpenAI.
- Trình soạn thảo trực quan WYSIWYG cho toàn bộ loại nội dung.
- Phân quyền tổ chức nhiều vai trò ngoài người học và quản trị viên cấu hình.

## Open Questions

- Không có.

## Acceptance Criteria

- [ ] AC-1: Tài khoản mới có thể bỏ qua kiểm tra và thấy Ngày 1, HSK 1, độ khó 1.
- [ ] AC-2: Bundle sai phạm vi hoặc trùng lặp không được phát hành và xuất hiện trong hàng đợi.
- [ ] AC-3: Quota chặn lượt vượt giới hạn trước khi gọi AI và usage ghi lại lượt thành công/thất bại.
- [ ] AC-4: Người không phải admin nhận 403; admin xem usage và quản lý được bản nháp.
- [ ] AC-5: Kết quả phát âm hiển thị từng âm tiết, thanh điệu, mẹo Việt và cảnh báo giới hạn.
- [ ] AC-6: Dashboard có 7 ngày hoạt động, ghi nhớ 30 ngày, kỹ năng yếu và một gợi ý ôn.
- [ ] AC-7: Analytics lỗi không ngăn người học tiếp tục lộ trình.
- [ ] AC-8: Kết quả học tiếp tục quyết định củng cố hoặc tăng cấp HSK.
