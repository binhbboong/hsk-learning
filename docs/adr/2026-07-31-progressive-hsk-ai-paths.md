# ADR: Lộ trình AI tăng dần từ HSK 1 đến HSK 6

Date: 2026-07-31
Slug: progressive-hsk-ai-paths
Status: Superseded by 2026-08-01-level-exam-promotion-gate (promotion gate only)
Related spec: docs/specs/ai-daily-paths/Specification.md

## Context

Spec `ai-daily-paths` ban đầu chỉ mở rộng số lượng bài trong HSK 1 và xác định việc tự động
chuyển từ HSK 1 sang HSK 2 là ngoài phạm vi. Hướng này không đáp ứng mục tiêu sản phẩm đã
được phê duyệt trong Vision và PRD: người Việt mới học cần một lộ trình có cấu trúc từ
HSK 1 đến HSK 6. Nếu AI chỉ tiếp tục tạo bài HSK 1, độ khó có thể đứng yên, lặp lại hoặc tăng
không kiểm soát mà không tạo ra tiến bộ theo cấp.

## Decision

Lộ trình hằng ngày do AI tạo sẽ tăng độ khó có kiểm soát trong từng cấp và đưa người học
tuần tự qua HSK 1, HSK 2, HSK 3, HSK 4, HSK 5 và HSK 6. Mỗi bài thuộc đúng một cấp HSK;
việc tăng độ khó và chuyển cấp phải dựa trên tiến độ, mức độ thành thạo và kết quả checkpoint,
không chỉ dựa trên số lần mở bài.

Mỗi cấp mới bắt đầu ở mức nhập môn của cấp đó, duy trì kiến thức tiền đề cần thiết và không
đưa kiến thức trọng tâm vượt cấp vào bài thường. Sau HSK 6, hệ thống dừng ở trạng thái hoàn
thành lộ trình HSK 1–6.

Điều kiện thành thạo để chuyển cấp là hoàn thành phạm vi nội dung của cấp hiện tại, đạt ít
nhất 80% điểm checkpoint cấp và đạt ít nhất 70% tỷ lệ ghi nhớ từ vựng của cấp hiện tại.

## Consequences

- Nội dung AI cần được kiểm soát theo phạm vi và độ khó của cả sáu cấp HSK.
- Hồ sơ học và dashboard phải thể hiện cấp hiện tại, tiến độ trong cấp và điều kiện chuyển
  cấp.
- Cơ chế tạo bài phải phân biệt giữa tăng độ khó, củng cố kiến thức yếu và chuyển cấp.
- Checkpoint trở thành cổng đánh giá thành thạo, không chỉ là bài kiểm tra sau mỗi 5 bài.
- Người học chưa đạt một trong hai ngưỡng phải tiếp tục nhận nội dung củng cố ở cấp hiện tại.
- Các tài liệu kiến trúc và đặc tả MVP chỉ giới hạn HSK 1 vẫn đúng với trạng thái hiện tại,
  nhưng không còn mô tả đầy đủ hướng phát triển của `ai-daily-paths`.
