# Specification: Bài thi tổng kết cấp HSK
Related UX: docs/ux/wireframes/hsk-level-exam.md

## Status

Approved

## Overview

HSK Learning cần một bài đánh giá tổng hợp ở cuối mỗi cấp HSK để người học biết mình đã sẵn
sàng chuyển cấp hay chưa. Bài thi xuất hiện sau khi người học hoàn thành Ngày hiện tại, checkpoint
và đạt điều kiện ghi nhớ; checkpoint sau mỗi 5 Bài vẫn được giữ nguyên.

Bài thi đánh giá từ vựng, ngữ pháp, đọc và nghe. Kết quả không phải chứng chỉ HSK chính thức,
nhưng được dùng làm điều kiện thăng cấp trong lộ trình của sản phẩm.

## User Scenarios

- Là người học đã hoàn thành một cấp, tôi muốn làm bài thi tổng kết để biết mình đã sẵn sàng lên cấp.
- Là người chưa đạt, tôi muốn thấy kỹ năng yếu và quay lại học củng cố trước khi thi lại.
- Là người đã đạt, tôi muốn tiếp tục Ngày đầu tiên của cấp HSK kế tiếp.
- Là người hoàn thành HSK 6, tôi muốn thấy xác nhận hoàn thành toàn bộ lộ trình.

## Functional Requirements

- FR-1: Hệ thống MUST yêu cầu bài thi tổng kết trước khi thăng từ HSK 1–5 lên cấp tiếp theo.
- FR-2: Hệ thống MUST yêu cầu bài thi HSK 6 trước khi xác nhận hoàn thành toàn bộ lộ trình.
- FR-3: Bài thi MUST chỉ mở khi người học hoàn thành 5 Bài và checkpoint của Ngày hiện tại,
  đồng thời đạt ít nhất 80% checkpoint và 70% ghi nhớ từ vựng.
- FR-4: Mỗi bài thi MUST có 20 câu: 5 từ vựng, 5 ngữ pháp, 5 đọc và 5 nghe.
- FR-5: Nội dung câu hỏi MUST nằm trong cấp HSK đang thi và ưu tiên kiến thức người học đã gặp.
- FR-6: Câu lựa chọn MUST có 4 đáp án và chỉ một đáp án đúng.
- FR-7: Câu nghe MUST phát được âm thanh mà không lộ transcript trước khi nộp.
- FR-8: Máy chủ MUST sở hữu đề, đáp án, thứ tự câu, trạng thái lượt thi và việc chấm điểm.
- FR-9: Một đề đã bắt đầu MUST không thay đổi giữa các lần tải lại hoặc thiết bị.
- FR-10: Người học MUST thấy tiến độ câu hiện tại, phần thi và thời gian đã làm; bài thi MUST
  không tự động nộp khi hết thời gian.
- FR-11: Người học MUST có thể đánh dấu câu để xem lại và chuyển giữa các câu chưa nộp.
- FR-12: Khi nộp bài, hệ thống MUST chấm tổng điểm và điểm từng kỹ năng.
- FR-13: Điểm đạt MUST là ít nhất 80% tổng số câu và không kỹ năng nào dưới 60%.
- FR-14: Kết quả MUST giải thích bằng tiếng Việt, chỉ ra tối đa hai kỹ năng cần củng cố và nêu
  rõ đây không phải điểm thi HSK chính thức.
- FR-15: Kết quả đạt MUST mở quyền tạo Ngày đầu tiên của HSK kế tiếp hoặc hoàn tất HSK 6.
- FR-16: Kết quả chưa đạt MUST giữ nguyên cấp hiện tại và đưa ra hành động học củng cố.
- FR-17: Người học MUST có thể thi lại ngay sau khi chưa đạt; mỗi lượt mới MUST dùng thứ tự câu khác.
- FR-18: Bài thi tổng kết MUST NOT tăng streak, tạo thẻ SRS hoặc đánh dấu Bài/checkpoint hoàn thành.
- FR-19: Kết quả và lượt đang làm MUST được lưu theo tài khoản để tiếp tục đa thiết bị.
- FR-20: Nếu chưa thể chuẩn bị đề hoặc audio, hệ thống MUST giữ nguyên tiến độ và cho phép thử lại.

## Out of Scope

- Mô phỏng chính xác cấu trúc, thời lượng hoặc chứng nhận của kỳ thi HSK chính thức.
- Thi nói HSKK hoặc chấm phát âm trong bài thi tổng kết.
- Giám sát chống gian lận bằng camera, khóa trình duyệt hoặc nhận diện danh tính.
- So sánh thứ hạng người học công khai.

## Open Questions

- Không có.

## Acceptance Criteria

- [ ] AC-1: Người đủ điều kiện thăng cấp thấy hành động “Thi tổng kết HSK N” thay vì tạo cấp mới.
- [ ] AC-2: Đề có đúng 20 câu và đúng 5 câu cho từng phần.
- [ ] AC-3: Payload trước khi nộp không chứa đáp án đúng hoặc transcript câu nghe.
- [ ] AC-4: Tải lại tiếp tục đúng đề, đáp án đã chọn và câu hiện tại.
- [ ] AC-5: Tổng điểm ≥80% nhưng một kỹ năng <60% vẫn chưa đạt.
- [ ] AC-6: Đạt HSK 1–5 mở cấp kế tiếp; đạt HSK 6 hoàn thành lộ trình.
- [ ] AC-7: Thi lại sau khi chưa đạt tạo lượt mới với thứ tự câu khác.
- [ ] AC-8: Làm/nộp bài thi không thay đổi streak, SRS hoặc tiến độ Bài.
- [ ] AC-9: Lỗi tạo đề/audio không tạo trạng thái thăng cấp một phần.
