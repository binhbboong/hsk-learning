# Implementation Plan: Vòng học bền vững
Spec: docs/specs/persistent-learning-loop/Specification.md

## Approach

Ba phương án được cân nhắc:

1. Lưu mọi thứ phía server ngay: đồng bộ tốt nhưng kéo theo auth, database và migration.
2. Rải `localStorage` trực tiếp trong từng component: nhanh nhưng khó version, test và dễ lệch.
3. Một repository hồ sơ local có schema version, kết hợp các domain service nhỏ cho progress,
   SRS, streak, mistakes và notebook. Chọn phương án 3 vì phù hợp ADR người dùng ẩn danh,
   test được bằng clock/storage giả và có đường migration sau này.

Lesson player dùng content contract mở rộng gồm dialogue lines, listening question,
sentence-order question và vocabulary. Các tính năng hiện có được tái sử dụng qua audio và
recording service; dashboard trở thành progress hub.

## File/Module Structure

| Path | Responsibility | Implements |
|---|---|---|
| `backend/hsk_api/models/learning_loop.py` | Schema 5 bài và checkpoint | Multi-activity lesson |
| `backend/hsk_api/content/learning_path.py` | Nội dung HSK 1 đã kiểm duyệt | Lesson/checkpoint |
| `backend/hsk_api/routers/learning_path.py` | Catalog, lesson, checkpoint endpoints | Dashboard/player |
| `frontend/src/app/core/models/learning-profile.ts` | Profile, SRS, mistakes, progress types | All |
| `frontend/src/app/core/services/learning-profile.repository.ts` | Versioned local persistence | All |
| `frontend/src/app/core/services/progress.service.ts` | Completion, next lesson, checkpoint | Dashboard/checkpoint |
| `frontend/src/app/core/services/streak.service.ts` | Daily streak transitions | Dashboard |
| `frontend/src/app/core/services/srs.service.ts` | Due scheduling and ratings | Review center |
| `frontend/src/app/core/services/mistake.service.ts` | Add/resolve wrong answers | Review center |
| `frontend/src/app/core/services/notebook.service.ts` | Personal vocabulary CRUD | Personal vocabulary |
| `frontend/src/app/features/learning-home/` | Progress dashboard | `learning-progress-dashboard.md` |
| `frontend/src/app/features/lesson-player/` | Dialogue and multi-activity flow | `multi-activity-lesson.md` |
| `frontend/src/app/features/review-center/` | SRS and mistakes | `review-center.md` |
| `frontend/src/app/features/checkpoint/` | Five-lesson test | `checkpoint-test.md` |
| `frontend/src/app/features/vocabulary-notebook/` | Personal vocabulary | `personal-vocabulary.md` |

## Testing Strategy

| Requirement | Verified by |
|---|---|
| FR-1–FR-8 | Lesson player/audio component tests |
| FR-9–FR-10 | Notebook service/component tests |
| FR-11–FR-14 | SRS service tests with fixed dates |
| FR-15–FR-16 | Mistake service/review tests |
| FR-17–FR-18 | Progress service/dashboard tests |
| FR-19–FR-20 | Streak tests with fixed dates |
| FR-21–FR-23 | Checkpoint service/component/E2E |
| FR-24–FR-26 | Repository corruption/reload and recording tests |
| FR-27 | Dashboard priority tests |

## Risks / Open Questions

- Local browser data is device-specific and can be cleared by the user.
- Date logic uses local calendar days; travel/timezone sync is out of scope.
- Speech synthesis voice availability differs by browser.
- Existing MVP routes remain as compatibility entry points until the new loop is verified.

## Related ADRs

- `docs/adr/2026-07-30-persistent-learning-loop.md`
