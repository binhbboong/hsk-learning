# Specification: Bài học ngữ pháp, nghe và phát âm
Related UX: docs/ux/prototypes/integrated-language-skills.md

## Status

Approved

## Overview

Người học hiện chỉ có thể hoàn thành bài từ vựng. Feature này mở rộng HSK 1 thành trải
nghiệm đa kỹ năng gồm ngữ pháp, nghe hiểu và phát âm, với giải thích tiếng Việt và phản hồi
phù hợp cho người Việt mới bắt đầu.

Mỗi bài kéo dài tối đa 10 phút, có thể học độc lập và kết thúc bằng kết quả cùng hành động
tiếp theo rõ ràng.

## User Scenarios

- As a người Việt mới học, I want hiểu mẫu câu qua giải thích tiếng Việt, so that tôi có thể
  dùng từ đã học trong câu đúng.
- As a người Việt mới học, I want nghe câu ở tốc độ thường và chậm, so that tôi nhận ra từ
  trong lời nói thật.
- As a người Việt mới học, I want ghi âm và nghe lại cách phát âm, so that tôi nhận biết và
  sửa lỗi thanh điệu thường gặp.
- As a người học, I want xem kết quả và gợi ý tiếp theo, so that tôi duy trì lộ trình.

## Functional Requirements

- FR-1: Hệ thống MUST hiển thị danh mục riêng cho Từ vựng, Ngữ pháp, Nghe hiểu và Phát âm.
- FR-2: Mỗi thẻ kỹ năng MUST cho biết mục tiêu, thời lượng và hành động bắt đầu.
- FR-3: Bài ngữ pháp MUST hiển thị mẫu câu, giải thích tiếng Việt và ít nhất hai ví dụ có chữ
  Hán, pinyin và nghĩa tiếng Việt.
- FR-4: Bài ngữ pháp MUST có ít nhất hai câu hỏi tương tác và phản hồi đúng/sai tức thời.
- FR-5: Người học MUST không thể chuyển câu ngữ pháp trước khi gửi đáp án hiện tại.
- FR-6: Bài nghe MUST cho phép phát cùng nội dung ở tốc độ thường và tốc độ chậm.
- FR-7: Transcript MUST được ẩn ban đầu và chỉ hiện khi người học chủ động yêu cầu hoặc sau
  khi gửi đáp án.
- FR-8: Bài nghe MUST có câu hỏi trắc nghiệm và phản hồi giải thích bằng tiếng Việt.
- FR-9: Nếu audio không khả dụng, hệ thống MUST cho phép hiện transcript và tiếp tục bài.
- FR-10: Bài phát âm MUST hiển thị chữ Hán, pinyin, nghĩa và hướng dẫn đường nét thanh điệu.
- FR-11: Bài phát âm MUST cho phép nghe mẫu.
- FR-12: Trên trình duyệt hỗ trợ microphone, người học MUST có thể ghi âm, dừng và nghe lại.
- FR-13: Nếu microphone bị từ chối hoặc không được hỗ trợ, người học MUST vẫn có thể hoàn
  thành bằng chế độ nghe mẫu và tự luyện.
- FR-14: Bài phát âm MUST nêu ít nhất một lỗi thường gặp của người Việt và một mẹo sửa cụ thể.
- FR-15: Người học MUST tự đánh giá phát âm theo ba mức trước khi hoàn thành.
- FR-16: Mỗi bài MUST kết thúc bằng kết quả, điểm/mức đánh giá và đề xuất học lại hoặc chọn
  kỹ năng khác.
- FR-17: Hệ thống MUST có trạng thái loading, error, empty và populated cho nội dung bài học.
- FR-18: Nội dung MUST giới hạn ở HSK 1 trong feature này và không tuyên bố thay thế giáo viên.

## Out of Scope

- Chấm điểm phát âm tự động từ waveform hoặc cam kết độ chính xác như giáo viên.
- Bài HSK 2–6 trong feature đầu tiên.
- Lưu audio của người học lên máy chủ.
- Tài khoản, đồng bộ nhiều thiết bị và bảng xếp hạng.
- Bài kiểm tra cấp HSK đầy đủ.

## Open Questions

- Không còn câu hỏi chặn implementation. Chấm âm tự động được xác định rõ là ngoài phạm vi
  của phiên bản này.

## Acceptance Criteria

- [ ] AC-1: Từ danh mục, người học có thể mở độc lập cả ba bài mới.
- [ ] AC-2: Người học hoàn thành hai câu ngữ pháp và nhận kết quả.
- [ ] AC-3: Người học phát audio thường/chậm, chỉ mở transcript khi cần và hoàn thành câu hỏi.
- [ ] AC-4: Người học ghi âm, nghe lại và tự đánh giá phát âm trên trình duyệt hỗ trợ.
- [ ] AC-5: Khi microphone không khả dụng, bài phát âm vẫn hoàn thành được.
- [ ] AC-6: Mỗi kết quả cho phép học lại hoặc quay về danh mục.
- [ ] AC-7: Mọi nội dung và phản hồi chính đều bằng tiếng Việt, bám HSK 1.
