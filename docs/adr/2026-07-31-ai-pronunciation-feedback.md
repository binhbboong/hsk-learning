# ADR: Dùng AI transcription cho phản hồi phát âm

Date: 2026-07-31
Slug: ai-pronunciation-feedback
Status: Accepted
Related spec: docs/specs/active-recall-pronunciation/Specification.md

## Context

Người mới cần biết câu mình vừa nói có được nhận diện đúng hay không. Trình duyệt hiện chỉ thu và phát lại âm thanh; việc tự tuyên bố chấm thanh điệu chính xác sẽ vượt quá khả năng đáng tin cậy của MVP.

## Decision

Backend gửi bản ghi tạm thời tới OpenAI speech-to-text với ngôn ngữ tiếng Trung, sau đó so transcript đã chuẩn hóa với câu mẫu để trả điểm, trạng thái và góp ý tiếng Việt. Không lưu bản ghi và không mô tả kết quả như điểm thi HSKK.

## Consequences

Phản hồi nhất quán, kiểm thử được và không cần lưu dữ liệu nhạy cảm. Tính năng cần API key, có chi phí/độ trễ mạng và chỉ đánh giá câu được nhận diện, chưa chấm chi tiết đường cao độ từng thanh.

