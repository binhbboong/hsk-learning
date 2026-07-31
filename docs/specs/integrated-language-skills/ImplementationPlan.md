# Implementation Plan: Bài học ngữ pháp, nghe và phát âm
Spec: docs/specs/integrated-language-skills/Specification.md

## Approach

Ba hướng được cân nhắc:

1. Ba mini-app độc lập: cô lập tốt nhưng lặp lại tải dữ liệu, kết quả và điều hướng.
2. Một engine bài học tổng quát theo schema động: mở rộng tốt nhưng quá phức tạp cho ba dạng
   tương tác rất khác nhau.
3. Một catalog và content API chung, mỗi kỹ năng có component/session service chuyên biệt,
   dùng chung result contract. Đây là lựa chọn được khuyến nghị vì giữ UI rõ ràng, test được
   từng kỹ năng và vẫn có điểm mở rộng hợp lý.

Nội dung HSK 1 được kiểm duyệt và trả từ FastAPI. Web Speech Synthesis phát mẫu nghe; bài
phát âm dùng MediaRecorder hoàn toàn trong trình duyệt, không tải audio người học lên server.
Nếu browser API không khả dụng, UI chuyển sang fallback đã mô tả trong wireframe.

## File/Module Structure

| Path | Responsibility | Implements |
|---|---|---|
| `backend/hsk_api/models/skills.py` | Schema catalog và nội dung ba kỹ năng | Prototype contract |
| `backend/hsk_api/content/default_skills.py` | Nội dung HSK 1 đã kiểm duyệt | All skill screens |
| `backend/hsk_api/routers/skills.py` | HTTP endpoints cho catalog và từng bài | Skills catalog |
| `backend/tests/test_skills_api.py` | Contract, empty/error boundary và HSK limit | FR-1–FR-3, FR-6–FR-18 |
| `frontend/src/app/core/models/skill-lesson.ts` | Typed client contracts | All skill screens |
| `frontend/src/app/core/services/skill-api.service.ts` | Load catalog và lesson | Loading/error/empty states |
| `frontend/src/app/core/services/audio.service.ts` | Speech synthesis và recording lifecycle | Listening/pronunciation |
| `frontend/src/app/core/services/skill-result.service.ts` | Result and retry navigation state | Skill results |
| `frontend/src/app/features/skills-catalog/` | Danh mục bốn kỹ năng | `skills-catalog.md` |
| `frontend/src/app/features/grammar/` | Hai câu hỏi và feedback loop | `grammar-practice.md` |
| `frontend/src/app/features/listening/` | Audio controls, transcript gate, answer | `listening-practice.md` |
| `frontend/src/app/features/pronunciation/` | Sample, record/playback, self-rating | `pronunciation-coach.md` |
| `frontend/src/app/features/skill-results/` | Kết quả và next actions | `skill-results.md` |
| `frontend/e2e/integrated-language-skills.spec.ts` | Full browser journeys | Prototype |

## Testing Strategy

| Requirement | Verified by |
|---|---|
| FR-1–FR-2 | API contract and catalog component tests |
| FR-3–FR-5 | Grammar API/component state-machine tests |
| FR-6–FR-9 | Listening component tests with audio service fake |
| FR-10–FR-15 | Pronunciation component and recording fallback tests |
| FR-16 | Result service/component tests |
| FR-17 | Component loading/error/empty tests |
| FR-18 | Backend schema/content tests and visible-copy assertions |

## Risks / Open Questions

- Speech synthesis voice availability differs by device; tests assert invocation and fallback,
  not a specific installed voice.
- Microphone permission cannot be automated reliably in every CI environment; unit tests fake
  MediaRecorder and E2E covers the no-microphone path.
- Browser session state remains local and is not a long-term progress system.

## Related ADRs

- Existing Angular/FastAPI and API-contract ADRs remain applicable.
- No new costly-to-reverse infrastructure decision is introduced.
