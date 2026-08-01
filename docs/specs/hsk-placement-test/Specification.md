# Specification: HSK Placement Test

Status: Approved
Date: 2026-08-01

## Overview

HSK Learning cung cấp bài kiểm tra đầu vào tùy chọn cho người học đã biết tiếng Trung. Bài kiểm
tra đánh giá từ vựng, ngữ pháp, nghe và phát âm, điều chỉnh độ khó trong phạm vi HSK 1–6 và đề
xuất cấp bắt đầu. Người mới có thể bỏ qua để bắt đầu HSK 1 ngay. Kết quả đầu vào không được tính
là hoàn thành Bài, checkpoint hay hoạt động duy trì chuỗi ngày học.

## User stories

- Là người mới, tôi muốn bỏ qua bài đầu vào để học HSK 1 ngay.
- Là người đã học trước đây, tôi muốn được đánh giá ngắn gọn để không phải học lại nội dung quá dễ.
- Là người học Việt Nam, tôi muốn xem kết quả theo từng kỹ năng với giải thích tiếng Việt.
- Là người học, tôi muốn chấp nhận cấp đề xuất hoặc chủ động chọn cấp khác trước khi bắt đầu lộ trình.
- Là người học đang có tiến độ, tôi muốn thi lại để tham khảo mà không làm mất dữ liệu học.

## Functional requirements

- FR-1: Bài kiểm tra MUST là tùy chọn; bỏ qua MUST đưa tài khoản chưa có tiến độ về HSK 1.
- FR-2: Một lượt đầy đủ MUST có 20 câu: 5 từ vựng, 5 ngữ pháp, 5 nghe và 5 phát âm.
- FR-3: Mỗi nhóm kỹ năng MUST điều chỉnh độ khó câu tiếp theo trong HSK 1–6 theo câu trả lời trước.
- FR-4: Câu từ vựng và ngữ pháp MUST có 4 lựa chọn và chỉ một đáp án đúng.
- FR-5: Câu nghe MUST có âm thanh phát từng câu, 4 lựa chọn và không lộ bản chép trước khi nộp.
- FR-6: Câu phát âm MUST cho phép thu âm, nghe lại, thu lại và gửi phân tích AI.
- FR-7: Nếu không thể thu âm hoặc dịch vụ AI không sẵn sàng, người học MAY bỏ qua câu phát âm;
  kết quả MUST ghi rõ kỹ năng chưa được đánh giá đầy đủ và giảm độ tin cậy.
- FR-8: Máy chủ MUST sở hữu thứ tự câu, đáp án đúng, trạng thái thích ứng và việc chấm điểm.
- FR-9: Giao diện MUST hiển thị số câu hiện tại, tổng số câu và nhóm kỹ năng hiện tại.
- FR-10: Câu đã nộp MUST không thể sửa; máy chủ MUST trả câu tiếp theo hoặc kết quả hoàn tất.
- FR-11: Lượt đang làm MUST được lưu theo tài khoản và tiếp tục được trên thiết bị khác.
- FR-12: Kết quả MUST gồm điểm/ước lượng cho từng kỹ năng, cấp HSK đề xuất từ 1–6, độ tin cậy
  và giải thích ngắn bằng tiếng Việt.
- FR-13: Kết quả MUST nói rõ đây là gợi ý học tập, không phải điểm thi HSK chính thức.
- FR-14: Trước khi có tiến độ học có ý nghĩa, người học MUST có thể chấp nhận cấp đề xuất hoặc chọn
  một cấp HSK 1–6 khác.
- FR-15: Khi chọn HSK lớn hơn 1, hệ thống MUST chuẩn bị Ngày 1 gồm 5 Bài đúng cấp trước khi đổi
  điểm bắt đầu; nếu tạo lộ trình lỗi, lựa chọn MUST không được áp dụng một phần và MUST cho phép thử lại.
- FR-16: Sau khi đã hoàn thành Bài/checkpoint hoặc có lộ trình cá nhân, lượt thi lại MUST chỉ mang
  tính tham khảo và MUST NOT đặt lại hay ghi đè tiến độ.
- FR-17: Bài đầu vào MUST NOT tăng streak, đánh dấu Bài/checkpoint hoàn thành, tạo thẻ SRS hoặc
  thay đổi thống kê ghi nhớ.
- FR-18: Người học MUST có thể thi lại sau 30 ngày; lượt dang dở MAY khởi động lại ngay.
- FR-19: Bản thu MUST chỉ được dùng cho lần phân tích hiện tại và MUST NOT được lưu dài hạn.
- FR-20: Giao diện MUST hỗ trợ trạng thái tải, lỗi mạng, lỗi microphone, AI không sẵn sàng và thử lại.
- FR-21: Bài đầu vào MUST dùng Pinyin, tiếng Việt và mẹo lỗi phát âm thường gặp khi phù hợp.

## Non-goals

- Chứng nhận trình độ hoặc dự đoán chắc chắn kết quả thi HSK chính thức.
- Thay thế đánh giá trực tiếp của giáo viên.
- Đặt lại lịch sử học khi thi lại.
- Sinh tự do toàn bộ ngân hàng câu hỏi bằng AI trong mỗi lượt thi.

## Acceptance criteria

- [ ] AC-1: Tài khoản mới có thể chọn “Kiểm tra đầu vào” hoặc “Bắt đầu HSK 1”.
- [ ] AC-2: Lượt thi có đúng 20 câu, 5 câu cho mỗi kỹ năng, và độ khó thay đổi theo đáp án.
- [ ] AC-3: Đáp án đúng không xuất hiện trong payload câu hỏi trước khi người học nộp.
- [ ] AC-4: Tải lại hoặc đăng nhập trên thiết bị khác tiếp tục đúng câu đang làm.
- [ ] AC-5: Kết quả hiển thị bốn kỹ năng, cấp đề xuất, độ tin cậy và lưu ý không phải điểm chính thức.
- [ ] AC-6: Tài khoản chưa có tiến độ có thể áp dụng HSK 1–6; HSK >1 chỉ được áp dụng sau khi
  Ngày 1 tương ứng được tạo thành công.
- [ ] AC-7: Thi, bỏ qua hoặc áp dụng kết quả không làm tăng streak hay số Bài/checkpoint hoàn thành.
- [ ] AC-8: Tài khoản đã học chỉ nhận kết quả tham khảo và không thể ghi đè lộ trình hiện tại.
- [ ] AC-9: Thu âm có thể nghe lại/thu lại; lỗi AI có lối thoát rõ ràng và làm giảm độ tin cậy.
- [ ] AC-10: Sau khi hoàn tất, nút thi lại bị khóa đến đúng 30 ngày sau.
