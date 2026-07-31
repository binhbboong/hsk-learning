# Implementation Plan: Học thích nghi và vận hành nội dung
Spec: docs/specs/learning-intelligence-operations/Specification.md

## Approach

Ba hướng đã được cân nhắc:

1. Dịch vụ phân tích/vận hành độc lập: tách biệt tốt nhưng tăng triển khai và đồng bộ dữ liệu.
2. Mở rộng API và hồ sơ hiện tại: dùng chung tài khoản, profile và bundle; ít rủi ro tích hợp.
3. Chỉ làm phía trình duyệt: nhanh nhưng không bảo vệ nội dung, quota hoặc quyền quản trị.

Chọn hướng 2. FastAPI sở hữu quality gate, quota, usage, draft và quyền admin; Angular đọc API
phân tích và quản trị. Hồ sơ hiện tại được mở rộng tương thích ngược. `gpt-audio` được dùng cho
quan sát âm thanh vì tài liệu OpenAI xác nhận mô hình nhận audio input; JSON được kiểm tra bằng
schema ứng dụng vì mô hình không hỗ trợ Structured Outputs.

## File/Module Structure

| Path | Responsibility | Implements |
|---|---|---|
| `backend/hsk_api/models/content_ops.py` | Hợp đồng quality, usage và draft | Content operations |
| `backend/hsk_api/services/content_quality.py` | Kiểm tra phạm vi, đầy đủ và trùng lặp | FR-2–4 |
| `backend/hsk_api/repositories/accounts.py` | Lưu draft, usage và tra quyền | FR-5–10 |
| `backend/hsk_api/routers/admin.py` | API quản trị có xác thực | Content operations wireframe |
| `backend/hsk_api/models/analytics.py` | Hợp đồng insight 7/30 ngày | Learning insights |
| `backend/hsk_api/services/analytics.py` | Tổng hợp hoạt động, retention và điểm yếu | FR-14–19 |
| `backend/hsk_api/routers/analytics.py` | API insight tài khoản | Learning insights wireframe |
| `backend/hsk_api/models/pronunciation.py` | Kết quả âm tiết/thanh điệu | Pronunciation state |
| `backend/hsk_api/adapters/openai_pronunciation.py` | Phân tích audio và fallback có giới hạn | FR-11–13 |
| `frontend/src/app/features/learning-home/*` | Khối insight và gợi ý ôn | Learning insights wireframe |
| `frontend/src/app/features/content-admin/*` | Hàng đợi, sửa và quyết định | Content operations wireframe |
| `frontend/src/app/core/services/*` | Client analytics/admin | Both wireframes |

## Testing Strategy

| Requirement | Verified by |
|---|---|
| FR-1, FR-20 | Path API tests for a new profile and progression tests |
| FR-2–4 | Quality service and daily-path publication tests |
| FR-5–6 | Quota/usage repository and API tests |
| FR-7–10 | Admin API authorization, edit, approve and reject tests |
| FR-11–13 | Pronunciation model/adapter/API and UI tests |
| FR-14–18 | Analytics service/API and dashboard component tests |
| FR-19 | Dashboard component analytics-error test |

## Risks / Open Questions

- Audio analysis is probabilistic; UI must preserve the assistive disclaimer.
- PostgreSQL is required in production; SQLite remains limited to local development and tests.
- Admin emails are configuration, not a full role-management system.

## Related ADRs

- docs/adr/2026-07-31-beginner-first-learning-intelligence.md
- docs/adr/2026-07-31-postgresql-production-persistence.md
