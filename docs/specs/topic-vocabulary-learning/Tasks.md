# Tasks: Học từ vựng theo chủ đề

## Architecture and contracts

- [x] Ghi ADR cho nội dung phiên do server sở hữu và tiến độ do profile sở hữu.
- [x] Định nghĩa schema chủ đề, từ và phiên; kiểm tra đúng 10 từ duy nhất.
- [x] Thêm bảng persistence cho đề xuất gần nhất và các bundle phiên.

## Backend — test first

- [x] Viết API tests cho xác thực, ít nhất 5 đề xuất, refresh và fallback.
- [x] Viết service/repository tests cho phiên 10 từ, idempotency và tải lại.
- [x] Thêm danh mục dự phòng đã kiểm duyệt.
- [x] Thêm adapter OpenAI và bộ kiểm định nội dung theo cấp HSK.
- [x] Thêm service, repository methods, router và app composition.

## Frontend domain — test first

- [x] Viết tests cho migration/default của `topicVocabularyProgress`.
- [x] Viết tests máy trạng thái 10 flipcard → 10 câu hỏi 4 đáp án.
- [x] Viết tests cho đúng tự chuyển, sai chờ tiếp tục, tải lại tiếp tục phiên.
- [x] Viết tests tích hợp SRS không trùng và streak không ảnh hưởng lộ trình ngày.
- [x] Thêm models, API client và session service.

## Frontend UI — test first

- [x] Viết component tests cho danh mục, refresh, loading/error/fallback/empty.
- [x] Viết component tests cho flipcard, audio, quiz và hoàn thành.
- [x] Triển khai màn hình `/learn/topics` và responsive dark/light styles.
- [x] Thêm điểm vào từ dashboard lộ trình.

## Verification

- [x] Chạy toàn bộ pytest backend — 58 passed, 1 skipped (2026-08-01).
- [x] Chạy toàn bộ Angular unit tests — 91 passed (2026-08-01).
- [x] Chạy Angular production build — thành công (2026-08-01).
- [x] Kiểm tra thủ công luồng chọn chủ đề → 10 flipcard → 4 đáp án → tải lại/tiếp tục.
- [x] Cập nhật trạng thái spec/tasks theo bằng chứng kiểm thử mới.
