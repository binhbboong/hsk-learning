# Implementation Plan: HSK Placement Test

Status: Approved
Date: 2026-08-01

## Chosen approach

Máy chủ quản lý một placement attempt bền vững: ngân hàng câu hỏi đã kiểm duyệt, đáp án, chỉ số
câu và trạng thái thích ứng đều ở backend. Client chỉ nhận câu hiện tại, nộp một đáp án và nhận câu
tiếp theo. Cách này tránh lộ đáp án, tiếp tục đa thiết bị và cho phép thay thuật toán mà không phát
hành lại frontend.

Hai phương án không chọn:

1. Chấm hoàn toàn trên Angular: nhanh nhưng lộ đáp án và không đáng tin cậy.
2. Gửi toàn bộ 20 câu một lần: dễ cache nhưng không thích ứng thực sự theo câu trả lời.

## Backend

- Thêm models công khai cho trạng thái, câu hỏi, câu trả lời và kết quả placement.
- Thêm ngân hàng câu hỏi có cấu trúc cho HSK 1–6; audio nghe dùng Web Speech trên client từ câu
  tiếng Trung do server cung cấp, nhưng transcript không nằm trong payload công khai.
- Thêm `placement_attempts` vào repository PostgreSQL/SQLite, lưu JSON state và kết quả theo account.
- Thêm `PlacementService` chọn câu theo kỹ năng, điều chỉnh mức ±1, chấm điểm và tính confidence.
- Thêm router `/api/v1/placement` cho status/start/answer/pronunciation/accept.
- Tái sử dụng pronunciation analyzer cho upload audio; chỉ lưu điểm và phản hồi, không lưu blob.
- Khi áp dụng HSK >1, yêu cầu `DailyPathService` tạo atomically bundle `path_index=1`; chỉ cập nhật
  profile placement sau khi bundle hợp lệ đã được lưu.
- Sửa daily-path overview để bundle index 1 thay thế nhóm HSK 1 tĩnh; tài khoản không placement giữ
  hành vi hiện tại.

## Frontend

- Thêm models/client API placement.
- Thêm route `/learn/placement`, intro, runner bốn kỹ năng và result selector.
- Tái sử dụng recorder và speech synthesis của lesson player qua service nhỏ dùng chung nếu cần.
- Thêm CTA có điều kiện ở learning home và liên kết đánh giá lại khi đã có tiến độ.
- Không ghi bất kỳ placement event nào vào progress/SRS/streak client-side.

## Data and migration

- Bảng `placement_attempts`: id, account_id, status, state JSON, result JSON, started/completed timestamps.
- Profile JSON thêm `placementTest` và `startingLevel`; field mới là optional để tương thích dữ liệu cũ.
- Xóa tài khoản phải xóa placement attempts theo cascade/quy trình repository hiện hành.

## Testing strategy

- Unit: adaptive selection, no leaked answer, level/confidence calculation, skipped pronunciation.
- Repository: start/resume/complete/retake persistence cho SQLite và contract PostgreSQL.
- API: auth, 20-question flow, audio upload error, 30-day gate, accept/override/idempotency.
- Integration: apply HSK >1 only after generated path succeeds; no progress/streak mutation.
- Angular: CTA, resume, MCQ, recorder fallback, result and locked advisory states.
- Browser QA: new account skip; complete representative attempt; refresh/resume; apply result.
