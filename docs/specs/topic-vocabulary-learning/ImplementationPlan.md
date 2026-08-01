# Implementation Plan: Học từ vựng theo chủ đề

Spec: `docs/specs/topic-vocabulary-learning/Specification.md`

## Approach

### Phương án được chọn: nội dung phiên do server sở hữu, tiến độ nằm trong hồ sơ học

FastAPI tạo hoặc lấy danh sách chủ đề đề xuất theo cấp HSK hiện tại, lịch sử học và điểm yếu của
tài khoản. Khi người học chọn chủ đề, server tạo đúng 10 từ, kiểm định hợp đồng dữ liệu và lưu bundle
bất biến theo tài khoản + chủ đề + số phiên trước khi trả về. Nếu AI không khả dụng hoặc nội dung không
hợp lệ, dịch vụ dùng danh mục đã kiểm duyệt để người học vẫn bắt đầu được ngay.

Angular cung cấp một khu vực riêng gồm danh mục chủ đề và trình học hai giai đoạn: xem đủ 10 flipcard,
sau đó trả lời 10 câu trắc nghiệm 4 lựa chọn. Tiến độ đang học, kết quả theo chủ đề và hoạt động streak
được ghi vào learning profile hiện có; mỗi từ dùng ID chuẩn hóa để dùng chung thẻ SRS và sổ từ, không
tạo bản sao. Hoàn thành phiên không ghi vào `completedLessonIds` hay `checkpointResults`.

### Phương án đã cân nhắc

1. **Tạo và lưu toàn bộ ở trình duyệt:** nhanh nhất nhưng làm lộ luồng AI, không ổn định giữa thiết bị,
   không có kiểm định tin cậy và không đáp ứng đồng bộ tài khoản.
2. **Lưu cả nội dung AI trong learning profile:** ít bảng hơn nhưng profile phình to, client có thể ghi đè
   nội dung chuẩn và khó chống tạo trùng khi có nhiều yêu cầu đồng thời.
3. **Server sở hữu bundle, profile sở hữu tiến độ (chọn):** cần endpoint và persistence riêng nhưng giữ
   ranh giới nội dung/tiến độ rõ ràng, giảm chi phí AI và đáp ứng tải lại, đa thiết bị, chống trùng.

## Data and API Design

- `GET /api/v1/topic-vocabulary/recommendations?refresh=false`: trả ít nhất 5 chủ đề kèm lý do,
  số từ và tiến độ; `refresh=true` yêu cầu một danh sách mới và truyền lịch sử gần nhất cho generator.
- `POST /api/v1/topic-vocabulary/sessions`: nhận `topic_id`, trả phiên đang dở hoặc tạo/lưu một bundle
  mới gồm đúng 10 từ.
- Bundle dùng khóa duy nhất `(account_id, session_id)` và trường payload JSON có schema chặt chẽ.
- Profile bổ sung `topicVocabularyProgress`; dữ liệu cũ được mặc định thành mảng rỗng khi tải.
- ID từ là dạng chuẩn hóa theo chữ Hán, nên SRS/sổ từ dùng cùng một bản ghi dù từ đến từ Bài hay chủ đề.

## File/Module Structure

| Path | Responsibility | Implements |
|---|---|---|
| `backend/hsk_api/models/topic_vocabulary.py` | Hợp đồng chủ đề, từ, phiên và request/response | FR-2–12, FR-15–16, FR-20–22 |
| `backend/hsk_api/content/topic_vocabulary.py` | Danh mục dự phòng đã kiểm duyệt và bộ từ theo HSK | FR-5–8, FR-21 |
| `backend/hsk_api/adapters/openai_topic_vocabulary.py` | Sinh đề xuất và bundle có cấu trúc từ OpenAI | FR-2–7, FR-19–20 |
| `backend/hsk_api/services/topic_vocabulary.py` | Điều phối AI/fallback, chất lượng, chống trùng, tải lại phiên | FR-2–7, FR-14, FR-19–22 |
| `backend/hsk_api/repositories/accounts.py` | Lưu danh sách đề xuất gần nhất và bundle theo tài khoản | FR-15–16, FR-19 |
| `backend/hsk_api/routers/topic_vocabulary.py` | API có xác thực cho danh mục và phiên | FR-1–7, FR-16, FR-19, FR-21–22 |
| `backend/hsk_api/main.py` | Khởi tạo generator, service và router | FR-2, FR-19–21 |
| `backend/tests/test_topic_vocabulary_api.py` | Kiểm thử API, fallback, persistence và hợp đồng 10 từ | AC-1–2, AC-5, AC-7–8 |
| `frontend/src/app/core/models/topic-vocabulary.ts` | Kiểu dữ liệu cho đề xuất, từ và phiên | FR-2–12, FR-15–16 |
| `frontend/src/app/core/models/learning-profile.ts` | Tiến độ phiên/chủ đề và activity kind mới | FR-13–18 |
| `frontend/src/app/core/services/topic-vocabulary-api.service.ts` | Gọi API danh mục, refresh và bắt đầu/tiếp tục phiên | FR-2–6, FR-16, FR-19, FR-21 |
| `frontend/src/app/core/services/topic-vocabulary-session.service.ts` | Máy trạng thái flipcard/quiz, lưu tiến độ, SRS và streak | FR-6, FR-9–18 |
| `frontend/src/app/features/topic-vocabulary/*` | UI danh mục, flipcard, 4 đáp án và mọi trạng thái | FR-1–12, FR-15–16, FR-19, FR-22 |
| `frontend/src/app/features/learning-home/*` | Điểm vào khu học từ theo chủ đề | FR-1 |
| `frontend/src/app/app.routes.ts` | Route có xác thực `/learn/topics` | FR-1 |

## Testing Strategy

| Requirement | Verified by |
|---|---|
| FR-1–4 | Route/component tests hiển thị khu riêng, ít nhất 5 đề xuất, lý do và thao tác chọn |
| FR-5–8 | Schema/API tests xác nhận đúng HSK, đúng 10 từ duy nhất và đủ dữ liệu/audio action |
| FR-9–10 | Component tests kiểm tra mặt trước ẩn thông tin và mặt sau hiện đủ nội dung |
| FR-11–12 | Session/component tests cho 4 đáp án duy nhất, đúng tự chuyển, sai chờ tiếp tục |
| FR-13–14 | Service tests xác nhận upsert SRS theo ID chuẩn hóa và không nhân đôi sổ từ |
| FR-15–16 | Repository/profile tests tải lại, đăng nhập lại và tiếp tục đúng vị trí |
| FR-17–18 | Progress tests xác nhận cập nhật streak nhưng không sửa bài/checkpoint/cấp HSK |
| FR-19–20 | API tests refresh tránh toàn bộ danh sách gần nhất và loại nội dung AI sai schema/chất lượng |
| FR-21–22 | API/component tests mô phỏng AI lỗi và tất cả trạng thái tải, trống, lỗi, học, hoàn thành |

## Delivery Order

1. Khóa hợp đồng API, persistence và ADR.
2. Viết test backend thất bại, sau đó triển khai AI/fallback và API.
3. Viết test domain frontend thất bại, sau đó triển khai profile/session/SRS.
4. Viết test component thất bại, sau đó triển khai danh mục và trình flipcard/quiz.
5. Nối route/dashboard, chạy regression backend/frontend và production build.

## Risks and Controls

- AI có thể trả từ ngoài cấp hoặc thiếu trường: Pydantic + quality gate từ chối toàn bộ bundle và dùng
  fallback, không lưu dữ liệu một phần.
- Bộ từ dự phòng phải đủ 10 từ ở mọi chủ đề/cấp MVP: kiểm thử tham số hóa kiểm tra số lượng và duy nhất.
- Ghi profile liên tiếp khi tự chuyển có thể đua nhau: chỉ lưu tại các mốc lật/chọn/chuyển và dùng một
  máy trạng thái đồng bộ ở frontend.
- Audio AI không nên chặn việc học: nút nghe dùng speech endpoint hiện có; lỗi audio có thông báo cục bộ
  và không làm mất phiên.

## Related ADR

- `docs/adr/2026-08-01-server-owned-topic-vocabulary.md`
