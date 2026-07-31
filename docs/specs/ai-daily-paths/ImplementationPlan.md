# Implementation Plan: Lộ trình hằng ngày do AI tạo
Spec: docs/specs/ai-daily-paths/Specification.md

## Approach

### Phương án được chọn: chặng học do server sở hữu và lưu bất biến

Server lưu từng chặng theo tài khoản và chỉ số chặng. Chặng đầu tiên tiếp tục dùng nội dung
HSK 1 đã kiểm duyệt; các chặng sau được AI tạo theo một hợp đồng có cấu trúc, kiểm tra phạm
vi HSK rồi lưu trước khi trả về. Các endpoint đọc lộ trình hợp nhất chặng gốc và các chặng
đã tạo. Một khóa duy nhất theo tài khoản + chỉ số chặng bảo đảm yêu cầu tạo lặp lại trả về
cùng nội dung.

Frontend dùng danh sách bài khả dụng từ server thay vì giả định toàn bộ lộ trình có đúng
5 bài. Sau mỗi checkpoint, dashboard yêu cầu chặng kế tiếp, hiển thị trạng thái đang tạo,
và tải lại lộ trình khi thành công. Hồ sơ học hiện tại vẫn sở hữu tiến độ, SRS, lỗi sai,
sổ từ và kết quả checkpoint.

### Phương án đã cân nhắc

1. **Lưu chặng AI trong learning profile:** ít bảng dữ liệu hơn nhưng payload hồ sơ phình to,
   client có thể ghi đè nội dung và khó bảo đảm tạo idempotent khi nhiều thiết bị cùng yêu cầu.
2. **Không lưu, tạo lại từ prompt mỗi lần:** đơn giản nhất nhưng vi phạm yêu cầu nội dung ổn
   định, khó học lại và có chi phí AI lặp lại.
3. **Server lưu chặng bất biến (chọn):** thêm persistence và endpoint mới nhưng đáp ứng tốt
   nhất tính ổn định, đồng bộ và chống tạo trùng.

## File/Module Structure

| Path | Responsibility | Implements |
|---|---|---|
| `backend/hsk_api/models/learning_loop.py` | Hợp đồng chặng, tổng quan lộ trình và metadata độ khó/HSK | FR-1–4, FR-16, FR-18–20 |
| `backend/hsk_api/adapters/openai_daily_paths.py` | Tạo 5 bài và checkpoint có cấu trúc theo ngữ cảnh thành thạo | FR-3–4, FR-9–10, FR-18–22, FR-26 |
| `backend/hsk_api/services/daily_paths.py` | Điều phối cấp HSK, độ khó, điều kiện chuyển cấp và idempotency | FR-5–10, FR-18–28 |
| `backend/hsk_api/repositories/accounts.py` | Lưu và đọc chặng bất biến theo tài khoản + chỉ số | FR-7–8, FR-11, FR-15 |
| `backend/hsk_api/routers/learning_path.py` | Cung cấp tổng quan, bài, checkpoint và thao tác tạo chặng tiếp theo | FR-5–8, FR-12–16 |
| `backend/hsk_api/main.py` | Khởi tạo generator và dependency của daily path service | FR-6, FR-14 |
| `backend/tests/test_daily_paths_api.py` | Kiểm thử API/persistence/validation/eligibility | AC-1–8, AC-11–15 |
| `frontend/src/app/core/models/learning-content.ts` | Hợp đồng tổng quan lộ trình động và trạng thái thành thạo | FR-12, FR-19, FR-25 |
| `frontend/src/app/core/services/learning-path-api.service.ts` | Gọi API tổng quan, bài/checkpoint động và tạo chặng | FR-6–8, FR-13–16 |
| `frontend/src/app/core/services/progress.service.ts` | Tính bài/checkpoint tiếp theo theo số bài khả dụng | FR-5, FR-12, FR-16–17, FR-23–28 |
| `frontend/src/app/features/learning-home/*` | Hiển thị cấp, chặng, tiến độ, trạng thái tạo/lỗi/thử lại | `learning-progress-dashboard.md`; FR-12–14, FR-25 |
| `frontend/src/app/features/checkpoint/*` | Tải đúng checkpoint theo phạm vi bài và quay về luồng tạo chặng | `checkpoint-test.md`; FR-5–6, FR-13, FR-16 |
| `frontend/src/app/features/lesson-player/*` | Tải bài động và giữ khả năng học lại bài cũ | `multi-activity-lesson.md`; FR-2–4, FR-15, FR-19–22 |

## Testing Strategy

| Requirement | Verified by |
|---|---|
| FR-1–4 | Schema tests bảo đảm đúng 5 bài, đủ hoạt động, tiếng Việt và metadata cấp/độ khó |
| FR-5–6 | API tests từ chối tạo trước checkpoint và mở Bài 6 sau checkpoint hợp lệ |
| FR-7–8 | Repository/API tests gọi tạo hai lần và qua client mới vẫn nhận cùng bundle |
| FR-9–10 | Generator contract tests kiểm tra context học và mục tiêu bài không trùng |
| FR-11 | Profile regression tests bảo đảm tạo chặng không đổi progress/SRS/mistakes/notebook |
| FR-12–13 | Component tests cho CTA bài/checkpoint, loading, success và retry |
| FR-14 | API + component tests cho lỗi generator không tạo row và hiển thị thử lại |
| FR-15 | API/component tests mở bài cũ sau khi có chặng mới |
| FR-16 | API/component tests checkpoint có đúng phạm vi mỗi nhóm 5 bài |
| FR-17 | Progress service regression test cho nhiều hoàn thành cùng ngày |
| FR-18–22 | Validation tests loại bundle sai cấp/cấu trúc và kiểm tra difficulty metadata tăng |
| FR-23–24 | Mastery tests cho thứ tự HSK và ngưỡng checkpoint 80% + retention 70% |
| FR-25 | Dashboard component test hiển thị cấp/progress/ngưỡng |
| FR-26 | Generator/service test chặng đầu cấp mới có difficulty nhập môn |
| FR-27 | Service/component test HSK 6 hoàn thành không tạo HSK 7 |
| FR-28 | Service test không tăng cấp khi chỉ mở/bỏ qua bài |

## Risks / Open Questions

- Một lần tạo 5 bài đa hoạt động có thể chậm hoặc vượt giới hạn output; adapter cần timeout
  rõ ràng và không được lưu bundle chưa hoàn chỉnh.
- Chất lượng phân cấp HSK của nội dung AI cần quan sát và có bộ kiểm định nội dung rộng hơn
  schema trước khi phát hành sản xuất.
- Tỷ lệ ghi nhớ hiện được suy ra từ trạng thái SRS; cần ghi rõ công thức trong code và test
  để ngưỡng 70% có nghĩa ổn định.
- Architecture đã được cập nhật thành trạng thái implemented sau khi toàn bộ task và
  verification gate dưới đây được xác minh.

## Related ADRs

- `docs/adr/2026-07-31-progressive-hsk-ai-paths.md`
- `docs/adr/2026-07-31-server-owned-ai-paths.md`
