# Specification: Phiên học từ vựng đầu tiên

Related UX: docs/ux/prototypes/first-vocabulary-session.md

## Status

Approved

## Overview

Người Việt mới học tiếng Trung cần một điểm bắt đầu rõ ràng và một cách ôn từ vựng chủ động
thay vì chỉ đọc danh sách từ. Tính năng này cung cấp một phiên học HSK 1 ngắn, hướng dẫn
người học qua bài được đề xuất, flip-card và kết quả phiên học.

Phiên học phải vẫn hoạt động khi không có dịch vụ tạo nội dung phù hợp: nội dung HSK 1 mặc
định đã được kiểm soát là đường lui bắt buộc. Kết quả trong phiên giúp người học biết từ nào
đã nhớ và từ nào cần ôn lại.

## User Scenarios

- As a người Việt mới học tiếng Trung, I want thấy một bài HSK 1 được đề xuất, so that tôi
  biết bắt đầu từ đâu.
- As a người học từ vựng, I want tự nhớ trước khi lật flip-card, so that tôi luyện khả năng
  nhớ chủ động.
- As a người Việt, I want xem pinyin, âm Hán–Việt, nghĩa tiếng Việt và ví dụ, so that tôi
  hiểu và ghi nhớ từ trong ngữ cảnh quen thuộc.
- As a người học, I want đánh dấu đã nhớ hoặc chưa nhớ, so that kết quả phản ánh đúng phiên
  học của tôi.
- As a người học, I want ôn lại các từ chưa nhớ, so that tôi có thể củng cố ngay điểm yếu.

## Functional Requirements

- FR-1: The system MUST present a learning dashboard with a recommended HSK 1 vocabulary
  lesson and a clear action to begin.
- FR-2: The system MUST show the lesson goal, number of cards, estimated duration and
  learning support available before the session begins.
- FR-3: The first vocabulary session MUST contain exactly 5 cards.
- FR-4: Each card MUST include a Chinese word, pinyin, Sino-Vietnamese reading, Vietnamese
  meaning and one example with a Vietnamese translation.
- FR-5: Before a card is flipped, the system MUST hide the answer content other than the
  prompt intended to trigger active recall.
- FR-6: After a card is flipped, the system MUST reveal all answer content and MUST offer
  separate “Đã nhớ” and “Chưa nhớ” actions.
- FR-7: The system MUST NOT allow a card to be rated before it has been flipped.
- FR-8: The system MUST display the current card number and total card count throughout the
  study session.
- FR-9: After a card is rated, the system MUST advance to the next card until all cards in
  the current session have been rated.
- FR-10: When the last card is rated, the system MUST show the total completed cards, the
  number remembered, the number not remembered and the words that need review.
- FR-11: When at least one word is marked “Chưa nhớ”, the system MUST allow a review session
  containing only those words.
- FR-12: The system MUST allow the learner to return from session results to the learning
  dashboard.
- FR-13: The system MUST preserve the current session’s ratings while the application
  remains open in the same browser session.
- FR-14: The system MUST attempt to provide lesson content appropriate to the requested HSK
  level when lesson-generation capability is available.
- FR-15: When lesson-generation capability is unavailable, misconfigured, times out or
  returns invalid content, the system MUST provide a validated default HSK 1 lesson without
  preventing the learner from completing the flow.
- FR-16: The system MUST distinguish loading, empty, error and populated states for the
  dashboard, lesson preparation, study session and results.
- FR-17: User-visible explanations and controls in this flow MUST be available in Vietnamese.
- FR-18: The system MUST NOT expose service credentials or secret values in any
  user-visible response.

## Out of Scope

> Update 2026-07-31: user registration and multi-user accounts are now delivered by
> `docs/specs/user-accounts/Specification.md`; the original exclusion is retained as historical
> scope for this feature.

- User registration, login or multi-user accounts.
- Cross-device synchronization or long-term cloud persistence.
- Spaced-repetition scheduling beyond immediate review of cards marked “Chưa nhớ”.
- Lessons beyond the first HSK 1 vocabulary session.
- Full grammar, listening, speech recording or pronunciation scoring experiences.
- Social features, teacher replacement or exam-pass guarantees.
- Choosing or configuring a lesson-generation provider from the user interface.

## Open Questions

- None for the first MVP.

## Acceptance Criteria

- [ ] AC-1 (FR-1, FR-2): From the dashboard, a learner can reach the study session in no
  more than two explicit start actions and can see the session size before starting.
- [ ] AC-2 (FR-3, FR-4): The initial lesson contains exactly 5 complete cards, each with all
  required Vietnamese-learning fields and an example translation.
- [ ] AC-3 (FR-5, FR-6, FR-7): Answer fields and rating actions are unavailable before
  flipping; both rating actions are available afterward.
- [ ] AC-4 (FR-8, FR-9): Rating a revealed card advances progress exactly once and displays
  each card in the session.
- [ ] AC-5 (FR-10): Rating the fifth card opens results whose remembered and unremembered
  counts sum to 5 and whose review list matches the ratings.
- [ ] AC-6 (FR-11, FR-12): A learner can review only unremembered cards or return to the
  dashboard from results.
- [ ] AC-7 (FR-13): Navigating within the application during the same browser session does
  not discard the current session ratings.
- [ ] AC-8 (FR-14, FR-15): Valid generated lesson content is usable; missing, failed or
  invalid generation produces the complete default lesson and still reaches results.
- [ ] AC-9 (FR-16, FR-17): Each designed screen has explicit loading, empty, error and
  populated behavior, with learner-facing controls and explanations in Vietnamese.
- [ ] AC-10 (FR-18): Inspecting user-visible responses and built client assets reveals no
  service credential or secret value.
