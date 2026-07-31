# Specification: Vòng học bền vững
Related UX: docs/ux/prototypes/persistent-learning-loop.md

> Forward scope: `docs/specs/ai-daily-paths/Specification.md` mở rộng increment HSK 1 này
> bằng các chặng AI bất biến và tiến trình HSK 1–6.

## Status

Approved

## Overview

Feature này biến các bài HSK 1 hiện có thành một lộ trình có khả năng tiếp tục lâu dài. Người
học nghe hội thoại từng câu, kiểm soát pinyin/bản dịch, làm hoạt động nghe và sắp xếp câu,
ghi âm, lưu từ; hệ thống ghi nhận tiến độ, lịch ôn, streak, lỗi sai và checkpoint định kỳ.

## User Scenarios

- As a người học, I want tiếp tục đúng bài và nhìn thấy streak, so that tôi duy trì thói quen.
- As a người mới, I want bật/tắt pinyin và dịch, so that tôi giảm hỗ trợ dần.
- As a người học, I want hệ thống tự lên lịch từ cần ôn, so that tôi không phải tự nhớ lịch.
- As a người làm sai, I want ôn lại riêng lỗi của mình, so that tôi sửa điểm yếu.
- As a người học, I want lưu từ quan trọng, so that tôi có bộ từ cá nhân.

## Functional Requirements

- FR-1: Mỗi hội thoại MUST cho phép phát âm thanh riêng cho từng câu.
- FR-2: Người học MUST có thể bật/tắt Pinyin độc lập với bản dịch.
- FR-3: Trạng thái Pinyin và bản dịch MUST được giữ khi chuyển câu trong cùng bài.
- FR-4: Mỗi bài MUST có ít nhất một câu nghe chọn đáp án.
- FR-5: Transcript của câu nghe MUST ẩn trước khi trả lời hoặc chủ động mở.
- FR-6: Mỗi bài MUST có ít nhất một hoạt động sắp xếp từ thành câu.
- FR-7: Hoạt động sắp xếp MUST hỗ trợ chọn token, hoàn tác và gửi đáp án.
- FR-8: Bài phát âm MUST cho phép thu âm, dừng và nghe lại khi trình duyệt hỗ trợ.
- FR-9: Từ trong hội thoại MUST có thể thêm/xóa khỏi sổ từ cá nhân.
- FR-10: Sổ từ MUST hiển thị chữ Hán, Pinyin, nghĩa và bài nguồn.
- FR-11: Mỗi thẻ ôn MUST có ngày đến hạn và mức lặp.
- FR-12: Đánh giá “Quên”, “Khó”, “Nhớ” MUST tạo khoảng ôn lần lượt 1, 3 và 7 ngày ở lần đầu.
- FR-13: Trả lời “Nhớ” nhiều lần MUST tăng khoảng ôn; “Quên” MUST đặt lại mức lặp.
- FR-14: Trung tâm ôn MUST chỉ hiển thị thẻ đến hạn, trừ khi người học chủ động ôn sổ từ.
- FR-15: Câu trả lời sai MUST được thêm vào hàng đợi ôn sai cùng đáp án và giải thích.
- FR-16: Trả lời đúng câu trong chế độ ôn sai MUST xóa câu đó khỏi hàng đợi.
- FR-17: Hệ thống MUST lưu tiến độ hoàn thành theo từng bài.
- FR-18: Dashboard MUST hiển thị số bài hoàn thành, bài tiếp theo và tỷ lệ hoàn thành.
- FR-19: Hoàn thành ít nhất một hoạt động trong ngày MUST cập nhật chuỗi ngày học.
- FR-20: Học vào ngày kế tiếp MUST tăng streak; bỏ qua một hoặc nhiều ngày MUST đặt streak về 1.
- FR-21: Sau mỗi 5 bài hoàn thành MUST mở khóa một checkpoint cho đúng nhóm bài đó.
- FR-22: Checkpoint MUST có ít nhất một câu nghe, một câu từ/nghĩa và một câu sắp xếp.
- FR-23: Kết quả checkpoint MUST lưu điểm và đưa mọi câu sai vào hàng đợi ôn sai.
- FR-24: Toàn bộ hồ sơ học MUST còn sau khi đóng/mở trình duyệt trên cùng thiết bị.
- FR-25: Dữ liệu lưu hỏng MUST được phục hồi về trạng thái an toàn mà không làm ứng dụng trắng.
- FR-26: Bản ghi microphone MUST NOT được lưu lâu dài hoặc gửi lên máy chủ.
- FR-27: Dashboard MUST ưu tiên checkpoint đang chờ, sau đó mục đến hạn, sau đó bài tiếp theo.

## Out of Scope

> Update 2026-07-31: the account exclusion below is superseded by
> `docs/specs/user-accounts/Specification.md`.

- Đồng bộ nhiều thiết bị hoặc tài khoản.
- Push notification nhắc học.
- Chấm waveform phát âm tự động.
- Nội dung HSK 2–6 trong vòng triển khai đầu.
- Xếp hạng xã hội.

## Open Questions

- Không còn câu hỏi chặn; dữ liệu local được chấp nhận cho giai đoạn người dùng ẩn danh.

## Acceptance Criteria

- [ ] AC-1: Hoàn thành một bài đa hoạt động cập nhật tiến độ và streak sau khi reload.
- [ ] AC-2: Pinyin và bản dịch bật/tắt độc lập trong hội thoại.
- [ ] AC-3: Câu nghe và sắp xếp câu tạo phản hồi; câu sai xuất hiện ở chế độ ôn sai.
- [ ] AC-4: Từ đã lưu xuất hiện trong sổ từ và có thể xóa/ôn.
- [ ] AC-5: Thẻ SRS được lên lịch đúng cho Quên/Khó/Nhớ và chỉ xuất hiện khi đến hạn.
- [ ] AC-6: Sau 5 bài, checkpoint được ưu tiên trên dashboard.
- [ ] AC-7: Làm sai checkpoint đưa câu vào ôn sai.
- [ ] AC-8: Microphone fallback không chặn hoàn thành bài và audio không được lưu lâu dài.
