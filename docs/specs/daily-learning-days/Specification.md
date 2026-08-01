# Specification: Lộ trình học theo Ngày
Related UX: docs/ux/prototypes/daily-learning-days.md

## Status

Approved

## Overview

Người học cần nhìn các nhóm 5 Bài hiện có như Ngày 1, Ngày 2… để hiểu rõ mình đang ở đâu
và điều kiện đi tiếp. Mỗi Ngày kết thúc bằng checkpoint, sau đó Ngày tiếp theo được mở ngay
mà không yêu cầu chờ sang ngày lịch tiếp theo.

## User Scenarios

- Là người mới học HSK, tôi muốn thấy Bài được nhóm theo Ngày để biết mục tiêu học hiện tại.
- Là người đã hoàn thành một Ngày, tôi muốn học Ngày tiếp theo ngay khi còn thời gian.
- Là người quay lại học, tôi muốn thấy đúng Ngày đang học và có thể xem lại các Ngày cũ.
- Là người chưa đạt ngưỡng tăng cấp, tôi muốn vẫn có Ngày tiếp theo để củng cố cùng cấp HSK.

## Functional Requirements

- FR-1: Hệ thống MUST gọi mỗi nhóm đúng 5 Bài và một checkpoint là một Ngày.
- FR-2: Ngày MUST được đánh số liên tục bắt đầu từ Ngày 1.
- FR-3: Bài MUST giữ số liên tục giữa các Ngày.
- FR-4: Tổng quan lộ trình MUST cung cấp danh sách Ngày với cấp HSK, độ khó, phạm vi Bài,
  tiến độ Bài và trạng thái checkpoint.
- FR-5: Dashboard MUST hiển thị rõ Ngày hiện tại, cấp HSK, độ khó và tiến độ x/5 Bài.
- FR-6: Dashboard MUST nhóm từng Bài dưới đúng Ngày của Bài đó.
- FR-7: Ngày hoàn thành MUST được phân biệt với Ngày đang học.
- FR-8: Người học MUST có thể mở lại Bài thuộc Ngày đã hoàn thành.
- FR-9: Checkpoint MUST thuộc đúng Ngày và ghi rõ phạm vi 5 Bài.
- FR-10: Hoàn thành 5 Bài nhưng chưa hoàn thành checkpoint MUST NOT mở Ngày kế tiếp.
- FR-11: Hoàn thành checkpoint của Ngày N MUST mở quá trình tạo hoặc cung cấp Ngày N+1 ngay.
- FR-12: Hệ thống MUST NOT buộc người học chờ sang ngày lịch tiếp theo để học Ngày N+1.
- FR-13: Hoàn thành nhiều Ngày học trong cùng ngày lịch MUST NOT tăng streak nhiều lần.
- FR-14: Khi đang tạo Ngày mới, dashboard MUST hiển thị số Ngày đang được chuẩn bị và ngăn
  yêu cầu tạo lặp.
- FR-15: Khi tạo Ngày mới thất bại, dashboard MUST giữ nguyên tiến độ, giải thích bằng tiếng
  Việt và cho phép thử lại.
- FR-16: Nếu kết quả chưa đạt ngưỡng tăng cấp, Ngày tiếp theo MUST tiếp tục cùng cấp HSK với
  nội dung củng cố khó hơn hoặc tập trung điểm yếu.
- FR-17: Nếu đạt ngưỡng checkpoint/ghi nhớ, hệ thống MUST yêu cầu bài thi tổng kết; sau khi
  đạt bài thi, Ngày tiếp theo MUST bắt đầu cấp HSK mới ở độ khó nhập môn.
- FR-18: Hoàn thành HSK 6 và đạt bài thi tổng kết MUST hiển thị trạng thái hoàn tất thay vì tạo thêm Ngày.

## Out of Scope

- Gắn Ngày học với một ngày/tháng/năm cụ thể.
- Giới hạn người học chỉ được hoàn thành một Ngày học mỗi ngày lịch.
- Thay đổi cách tính streak hiện tại.
- Thay đổi cấu trúc hoạt động bên trong từng Bài.
- Cấu trúc nội bộ bài thi tổng kết hoặc bài kiểm tra đầu vào; chúng thuộc các đặc tả riêng
  `hsk-level-exams` và `hsk-placement-test`. Cấu trúc một Ngày vẫn không đổi.

## Open Questions

Không có.

## Acceptance Criteria

- [ ] AC-1: Lộ trình mới hiển thị Ngày 1 chứa Bài 1–5 và checkpoint Bài 1–5.
- [ ] AC-2: Sau khi có Bài 6–10, dashboard hiển thị Ngày 2 với tiến độ riêng x/5.
- [ ] AC-3: Hoàn thành Bài 10 dẫn đến checkpoint Bài 6–10.
- [ ] AC-4: Hoàn thành checkpoint Ngày 2 có thể mở Ngày 3 ngay trong cùng ngày lịch.
- [ ] AC-5: Hai Ngày hoàn thành cùng ngày lịch chỉ tăng streak một lần.
- [ ] AC-6: Tải lại trang vẫn giữ đúng số Ngày và nội dung từng Ngày.
- [ ] AC-7: Lỗi tạo Ngày 3 vẫn giữ Ngày 1–2 và hiển thị nút thử lại.
- [ ] AC-8: Bài thuộc Ngày hoàn thành vẫn mở lại được.
- [ ] AC-9: Ngày củng cố giữ nguyên cấp HSK và tăng độ khó.
- [ ] AC-10: Sau khi đạt bài thi tổng kết, Ngày tăng cấp hiển thị cấp HSK mới và độ khó nhập môn.
