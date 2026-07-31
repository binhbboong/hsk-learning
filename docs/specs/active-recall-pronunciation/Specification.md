# Specification: Ôn 4 đáp án và phản hồi phát âm AI

Status: Approved

## Mục tiêu

Biến lượt ôn từ vựng thành bài nhớ chủ động và giúp người mới nhận phản hồi tức thời sau khi tự thu âm một câu tiếng Trung.

## Yêu cầu chức năng

- FR-01: Mỗi thẻ ôn hiển thị Hán tự, Pinyin và đúng 4 nghĩa tiếng Việt không trùng nhau.
- FR-02: Một câu chỉ có một đáp án đúng. Sau khi chọn, đáp án bị khóa và giao diện chỉ rõ đúng/sai cùng nghĩa đúng.
- FR-03: Khi người học bấm “Câu tiếp theo”, câu đúng được xếp lịch như `remembered`; câu sai như `forgot`.
- FR-04: Cơ chế 4 đáp án áp dụng cho ôn ngắt quãng và sổ từ cá nhân.
- FR-05: Sau khi thu âm trong bài học, người học có thể gửi bản ghi để AI phân tích.
- FR-06: Kết quả gồm trạng thái đúng/cần luyện thêm, điểm 0–100, câu AI nghe được và góp ý tiếng Việt.
- FR-07: Khi AI chưa được cấu hình hoặc lỗi, người học vẫn nghe lại bản ghi và hoàn thành bài.
- FR-08: Bản ghi được xử lý trong bộ nhớ, không lưu vào hồ sơ hay cơ sở dữ liệu.

## Tiêu chí nghiệm thu

1. Mỗi câu ôn có 4 lựa chọn duy nhất và chính xác một lựa chọn đúng.
2. Chọn sai làm thẻ đến hạn lại sau 1 ngày; chọn đúng dùng lịch nhớ hiện có.
3. Không thể đổi lựa chọn sau khi đã trả lời.
4. File WebM/WAV/MP3 hợp lệ, tối đa 5 MB, được gửi qua API có xác thực.
5. Kết quả AI hiển thị cạnh phần nghe lại; lỗi AI không chặn nút hoàn thành.

## Ngoài phạm vi

- Chấm điểm chuẩn kỳ thi HSK/HSKK hoặc bảo đảm độ chính xác tuyệt đối của thanh điệu.
- Lưu lịch sử bản thu âm.
- Huấn luyện mô hình giọng nói riêng.

