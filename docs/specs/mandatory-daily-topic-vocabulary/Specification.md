# Specification: Phiên từ vựng chủ đề bắt buộc theo Ngày
Related UX:
- docs/ux/prototypes/daily-learning-days.md
- docs/ux/wireframes/learning-progress-dashboard.md

## Status

Approved

## Overview

Mỗi Ngày học phải bảo đảm người học không chỉ hoàn thành 5 Bài đa kỹ năng mà còn xây vốn từ theo
một ngữ cảnh tự chọn. Người học chọn một trong các chủ đề AI đề xuất, hoàn thành đúng 10 từ bằng
flipcard và trắc nghiệm, rồi mới được làm checkpoint của Ngày.

Thay đổi này đưa phiên chủ đề vào lộ trình bắt buộc nhưng vẫn giữ phiên là một loại hoạt động riêng,
không đổi số Bài, không đổi cách đánh số Bài và không tự thay đổi cấp HSK.

## User Scenarios

- Là người mới học HSK, tôi muốn thấy rõ phiên 10 từ là một bước của Ngày để không bỏ sót phần xây vốn từ.
- Là người học có sở thích khác nhau, tôi muốn tự chọn chủ đề từ các đề xuất AI phù hợp cấp HSK.
- Là người vừa hoàn thành 5 Bài, tôi muốn được dẫn thẳng tới bước 10 từ trước checkpoint.
- Là người quay lại học, tôi muốn trạng thái hoàn thành phiên chủ đề của từng Ngày được giữ nguyên.

## Functional Requirements

- FR-1: Mỗi Ngày MUST gồm đúng 5 Bài, một phiên 10 từ theo chủ đề và một checkpoint.
- FR-2: Người học MUST được chọn chủ đề từ danh sách AI đề xuất hoặc danh mục dự phòng phù hợp cấp HSK.
- FR-3: Sau khi hoàn thành 5 Bài nhưng chưa đủ phiên chủ đề, hành động tiếp theo MUST dẫn tới khu chọn chủ đề.
- FR-4: Checkpoint của Ngày MUST NOT được mở trước khi hoàn thành cả 5 Bài và một phiên đúng 10 từ.
- FR-5: Một phiên chủ đề hoàn thành MUST chỉ đáp ứng tối đa một Ngày.
- FR-6: Các phiên hoàn thành MUST được phân bổ tuần tự cho các Ngày để dữ liệu hiện có tiếp tục có hiệu lực.
- FR-7: Tổng quan Ngày MUST cho biết bước chủ đề đã hoàn thành hay còn bắt buộc.
- FR-8: Ngày MUST chỉ có trạng thái hoàn thành khi đủ 5 Bài, phiên chủ đề và checkpoint.
- FR-9: Hệ thống MUST NOT tạo Ngày kế tiếp nếu Ngày hiện tại chưa đủ phiên chủ đề bắt buộc.
- FR-10: Hoàn thành phiên chủ đề MUST tiếp tục cập nhật SRS và streak theo quy tắc hiện hành.
- FR-11: Phiên chủ đề MUST NOT được tính là một Bài và MUST NOT tự thay đổi cấp HSK.
- FR-12: Sau khi hoàn thành phiên bắt buộc, người học MUST có hành động rõ ràng để quay lại lộ trình và làm checkpoint.

## Out of Scope

- Thay đổi nội dung 10 flipcard hoặc 10 câu trắc nghiệm hiện có.
- Tự động chọn chủ đề thay cho người học.
- Tăng số Bài của một Ngày hoặc đổi cách đánh số Bài.
- Thay đổi thuật toán SRS, streak hoặc điều kiện thăng cấp HSK khác.

## Open Questions

Không có.

## Acceptance Criteria

- [ ] AC-1: Ngày hiển thị riêng tiến độ 5 Bài, phiên 10 từ và checkpoint.
- [ ] AC-2: Sau Bài thứ 5, CTA dẫn tới chọn chủ đề nếu chưa có phiên hoàn thành cho Ngày.
- [ ] AC-3: Checkpoint bị khóa cho tới khi phiên 10 từ hoàn thành.
- [ ] AC-4: Hoàn thành phiên làm CTA tiếp theo chuyển thành checkpoint.
- [ ] AC-5: Hoàn thành checkpoint sau đủ ba bước mở được Ngày kế tiếp.
- [ ] AC-6: API từ chối tạo Ngày kế tiếp nếu thiếu phiên chủ đề.
- [ ] AC-7: Hồ sơ có N phiên chủ đề hoàn thành ghi nhận tối đa N Ngày đã đủ bước chủ đề.
- [ ] AC-8: Tải lại hoặc đăng nhập lại vẫn giữ đúng trạng thái bắt buộc của từng Ngày.
