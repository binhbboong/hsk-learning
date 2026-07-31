# Implementation Plan

## Hướng kỹ thuật

- Angular tạo 4 lựa chọn từ hàng đợi ôn và một tập nghĩa HSK dự phòng, xáo trộn ổn định theo mã thẻ.
- `ReviewCenter` giữ phản hồi sai trên màn hình để người học xem lại; với đáp án đúng, hiển thị phản hồi ngắn rồi tự cập nhật SRS và chuyển sang thẻ tiếp theo.
- `AudioService` giữ Blob cuối cùng ngoài URL nghe lại.
- FastAPI nhận multipart có xác thực, kiểm tra loại/kích thước và gọi bộ phân tích phát âm.
- Bộ phân tích dùng OpenAI transcription tiếng Trung, chuẩn hóa transcript và so độ tương đồng với câu mẫu để trả kết quả nhất quán.

## Tệp chính

- `frontend/src/app/core/services/review-quiz.service.ts`
- `frontend/src/app/features/review-center/*`
- `frontend/src/app/core/services/pronunciation-analysis.service.ts`
- `frontend/src/app/features/lesson-player/*`
- `backend/hsk_api/adapters/openai_pronunciation.py`
- `backend/hsk_api/routers/pronunciation.py`

## Kiểm thử

- Unit test tạo đáp án, trạng thái đúng/sai và cập nhật SRS.
- API test xác thực, multipart, giới hạn file và kết quả bộ phân tích giả.
- Component test gửi Blob và hiển thị phản hồi AI.
- Chạy toàn bộ pytest, Angular tests và production build.
