# Implementation Plan: Bài thi tổng kết cấp HSK
Spec: docs/specs/hsk-level-exams/Specification.md

## Approach

Ba hướng đã cân nhắc:

1. Chấm toàn bộ ở frontend: nhanh nhưng lộ đáp án, khó tiếp tục đa thiết bị và không đủ tin cậy
   để khóa thăng cấp.
2. Tạo đề mới theo từng request: linh hoạt nhưng dễ đổi đề giữa lượt, tốn AI và có rủi ro trạng thái
   thăng cấp một phần.
3. Máy chủ tạo/lưu snapshot đề, lưu lượt và chấm server-side: thêm persistence nhưng bảo đảm tính
   nhất quán, riêng tư đáp án và khả năng audit.

Chọn phương án 3. Đề 20 câu được tổng hợp từ chính năm Bài của Ngày vừa hoàn thành ở mọi cấp HSK,
giúp bám nội dung đã học và không phụ thuộc thêm một lượt gọi AI. Mỗi đề được lưu bất biến trước khi bắt đầu lượt thi.

## File/Module Structure

| Path | Responsibility | Implements |
|---|---|---|
| `backend/hsk_api/models/level_exam.py` | Hợp đồng đề, lượt thi và kết quả | FR-4, FR-8, FR-12 |
| `backend/hsk_api/services/level_exams.py` | Blueprint từ 5 Bài vừa học, eligibility, chấm, retake | FR-1–FR-20 |
| `backend/hsk_api/routers/level_exams.py` | API authenticated và audio | FR-7–FR-20 |
| `backend/hsk_api/repositories/accounts.py` | Lưu đề/lượt/kết quả | FR-9, FR-19 |
| `backend/hsk_api/services/daily_paths.py` | Gate thăng cấp bằng kết quả thi | FR-1, FR-2, FR-15 |
| `frontend/src/app/core/models/level-exam.ts` | Kiểu dữ liệu client | Wireframe toàn luồng |
| `frontend/src/app/core/services/level-exam-api.service.ts` | Gọi API bài thi/audio | Wireframe toàn luồng |
| `frontend/src/app/features/level-exam/*` | Intro, runner, kết quả | `hsk-level-exam.md` |
| `frontend/src/app/core/services/progress.service.ts` | Chọn hành động thi trước thăng cấp | AC-1 |
| `frontend/src/app/features/learning-home/*` | Điểm vào bài thi | AC-1 |

## Testing Strategy

| Requirement | Verified by |
|---|---|
| FR-1–FR-3 | Daily-path/API eligibility and promotion tests |
| FR-4–FR-7 | Blueprint, response privacy and audio API tests |
| FR-8–FR-12 | Attempt persistence, resume, navigation and scoring tests |
| FR-13–FR-17 | Threshold, result, promotion and retake tests |
| FR-18–FR-20 | Profile invariance, failure atomicity and UI error tests |

## Risks / Open Questions

- Chất lượng đề phụ thuộc chất lượng năm Bài nguồn; snapshot giúp giữ ổn định và truy vết.
- Chất lượng đề cần được quan sát và sau này đưa vào cùng hàng đợi quản trị nội dung.
- Listening audio tăng chi phí; đề và audio cần cache hợp lý nhưng không lưu bản ghi người học.

## Related ADRs

- `docs/adr/2026-08-01-level-exam-promotion-gate.md`
