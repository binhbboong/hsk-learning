# Specification: Học từ vựng theo chủ đề

## Status

Implemented

## Overview

Người học cần một khu vực học từ vựng độc lập với lộ trình bài học hằng ngày để có thể tập trung
vào những ngữ cảnh thiết thực. AI đề xuất các chủ đề phù hợp dựa trên cấp HSK, lịch sử học và điểm
yếu hiện tại; người học chọn một đề xuất để bắt đầu. Nội dung vẫn phải giữ độ khó, từ vựng và ví dụ
phù hợp với cấp HSK hiện tại.

Mỗi phiên theo chủ đề là một hoạt động bổ trợ ngắn, có tiến độ riêng và dùng chung lịch ôn từ của
người học. Hoàn thành phiên có thể duy trì chuỗi ngày học, nhưng không thay thế các bài bắt buộc
hoặc checkpoint trong lộ trình HSK 1–6.

## User Scenarios

- Là người Việt mới học tiếng Trung, tôi muốn xem danh sách chủ đề dễ hiểu để chọn nội dung hữu
  ích với mình.
- Là người chưa biết nên chọn chủ đề nào, tôi muốn AI đề xuất và giải thích lý do để quyết định
  nhanh hơn.
- Là người học chuẩn bị đi du lịch, tôi muốn học riêng nhóm từ về đi lại và ăn uống để có thể sử
  dụng trong tình huống thực tế.
- Là người học từ vựng, tôi muốn xem chữ Hán, Pinyin, âm Hán–Việt, nghĩa tiếng Việt, âm thanh và ví
  dụ để ghi nhớ từ trong ngữ cảnh.
- Là người đang học HSK, tôi muốn nội dung theo chủ đề vẫn phù hợp với cấp độ hiện tại để không bị
  quá tải bởi từ ngoài trình độ.
- Là người học đều đặn, tôi muốn từ đã học theo chủ đề xuất hiện trong lịch ôn chung để không quên
  sau khi kết thúc phiên.
- Là người quay lại một chủ đề, tôi muốn thấy tiến độ và tiếp tục từ phần chưa học.

## Functional Requirements

- FR-1: Hệ thống MUST cung cấp một khu vực từ vựng theo chủ đề tách biệt với lộ trình bài học hằng
  ngày.
- FR-2: Hệ thống MUST hiển thị các chủ đề do AI đề xuất cùng tên tiếng Việt, mô tả ngắn, lý do đề
  xuất, số từ và tiến độ của người học trong từng chủ đề.
- FR-3: Mỗi lần đề xuất MUST cung cấp ít nhất 5 chủ đề khác nhau, phù hợp với cấp HSK, lịch sử học
  hoặc điểm yếu hiện tại của người học.
- FR-4: Người học MUST chọn được một chủ đề được đề xuất và bắt đầu phiên từ vựng phù hợp với cấp
  HSK hiện tại.
- FR-5: Hệ thống MUST chỉ đưa vào phiên học các từ phù hợp với cấp HSK hiện tại của người học,
  ngoại trừ từ ngoài cấp được đánh dấu rõ là từ mở rộng.
- FR-6: Mỗi phiên học MUST chứa đúng 10 từ duy nhất chưa hoàn thành hoặc đang cần củng cố trong chủ đề được
  chọn.
- FR-7: Mỗi từ MUST có chữ Hán, Pinyin, âm Hán–Việt, nghĩa tiếng Việt, âm thanh mẫu, một câu ví dụ
  tiếng Trung và bản dịch tiếng Việt.
- FR-8: Người học MUST có thể phát âm thanh riêng cho từng từ và câu ví dụ.
- FR-9: Trong lượt học, hệ thống MUST hiển thị từng từ dưới dạng flipcard; mặt trước hiển thị chữ
  Hán và hành động nghe âm thanh nhưng MUST ẩn Pinyin, âm Hán–Việt, nghĩa và ví dụ.
- FR-10: Khi người học lật thẻ, mặt sau MUST hiển thị Pinyin, âm Hán–Việt, nghĩa tiếng Việt, câu ví
  dụ và bản dịch.
- FR-11: Sau khi người học đã xem đủ 10 flipcard, hệ thống MUST mở lượt nhớ chủ động; mỗi từ MUST
  có đúng 4 đáp án tiếng Việt không trùng nhau và chỉ một đáp án đúng.
- FR-12: Sau khi chọn đáp án, hệ thống MUST chỉ rõ đúng hoặc sai và hiển thị nghĩa đúng; đáp án đúng
  MUST tự chuyển sang từ tiếp theo sau phản hồi ngắn, còn đáp án sai MUST giữ phản hồi cho đến khi
  người học chủ động chuyển tiếp.
- FR-13: Từ hoàn thành trong phiên chủ đề MUST được đưa vào lịch ôn ngắt quãng chung của tài khoản.
- FR-14: Nếu một từ đã tồn tại trong lịch ôn hoặc sổ từ, hệ thống MUST dùng chung trạng thái học
  của từ đó và MUST NOT tạo mục trùng lặp.
- FR-15: Hệ thống MUST lưu số từ đã học, số từ đã nhớ và tỷ lệ hoàn thành riêng cho từng chủ đề.
- FR-16: Người học MUST có thể tiếp tục một chủ đề từ phần chưa hoàn thành trong lần truy cập sau
  và trên thiết bị khác khi đăng nhập cùng tài khoản.
- FR-17: Hoàn thành ít nhất một phiên theo chủ đề trong ngày MUST được tính là hoạt động duy trì
  streak.
- FR-18: Hoàn thành phiên theo chủ đề MUST NOT đánh dấu hoàn thành bài trong lộ trình hằng ngày,
  MUST NOT mở khóa checkpoint và MUST NOT thay đổi cấp HSK của người học.
- FR-19: Hệ thống MUST cho phép người học yêu cầu danh sách đề xuất chủ đề mới và MUST tránh lặp
  toàn bộ danh sách đề xuất gần nhất khi vẫn còn chủ đề phù hợp khác.
- FR-20: Nội dung theo chủ đề MUST tuân thủ cùng tiêu chuẩn kiểm soát phạm vi HSK, tính đầy đủ,
  trùng lặp và chất lượng tiếng Việt như nội dung lộ trình.
- FR-21: Khi AI chưa khả dụng hoặc không tạo được đề xuất hợp lệ, hệ thống MUST hiển thị các chủ đề
  dự phòng đã được kiểm soát, gồm ít nhất chào hỏi, gia đình, ăn uống, du lịch, mua sắm, trường học
  và công việc.
- FR-22: Khu vực chủ đề MUST có trạng thái đang tải, chưa có nội dung, lỗi, đang học, hoàn thành và
  đã học hết nội dung hiện có.

## Out of Scope

- Thay thế lộ trình HSK 1–6 hoặc checkpoint định kỳ.
- Cho phép học từ ngoài phạm vi tiếng Trung HSK mà không có nhãn từ mở rộng.
- Mạng xã hội, bảng xếp hạng hoặc chia sẻ bộ từ công khai.
- Cho phép người học tự sửa nội dung chuẩn của từ vựng.
- Cam kết nội dung theo chủ đề đủ cho một tình huống nghề nghiệp chuyên môn.
- Cho phép người học nhập chủ đề tùy ý; MVP chỉ cho chọn từ các chủ đề do AI đề xuất hoặc danh mục
  dự phòng đã được kiểm soát.

## Open Questions

- Không còn câu hỏi chặn lập kế hoạch.

## Acceptance Criteria

- [x] AC-1 (FR-1–FR-4): Người học mở được khu vực riêng, xem ít nhất 5 chủ đề AI đề xuất cùng lý do,
  tiến độ và bắt đầu một chủ đề phù hợp cấp HSK hiện tại.
- [x] AC-2 (FR-5–FR-8): Phiên học có đúng 10 từ duy nhất và hoàn chỉnh; từ ngoài cấp nếu có được đánh dấu rõ và
  từng từ/câu ví dụ phát được âm thanh.
- [x] AC-3 (FR-9–FR-12): Người học xem đủ 10 flipcard trước lượt nhớ chủ động; mỗi từ có 4 đáp án
  duy nhất, đáp án đúng tự chuyển từ và đáp án sai giữ phản hồi cho đến khi người học tiếp tục.
- [x] AC-4 (FR-13–FR-14): Hoàn thành phiên tạo lịch ôn cho các từ mới nhưng không tạo bản sao của
  từ đã có trong lịch ôn hoặc sổ từ.
- [x] AC-5 (FR-15–FR-16): Tải lại hoặc đăng nhập trên thiết bị khác vẫn hiển thị đúng tiến độ chủ
  đề và tiếp tục từ phần chưa hoàn thành.
- [x] AC-6 (FR-17–FR-18): Phiên chủ đề cập nhật streak nhưng không hoàn thành bài, mở checkpoint
  hoặc thay đổi cấp HSK.
- [x] AC-7 (FR-19–FR-20): Người học yêu cầu được danh sách đề xuất mới; nội dung phát hành vượt qua
  các kiểm tra chất lượng hiện hành.
- [x] AC-8 (FR-21–FR-22): Khi AI không khả dụng, người học vẫn chọn được chủ đề dự phòng; mọi trạng
  thái tải, trống, lỗi, học và hoàn thành đều có thông báo và hành động tiếp theo rõ ràng.
