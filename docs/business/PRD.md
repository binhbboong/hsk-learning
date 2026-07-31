# PRD: HSK Learning

Vision: docs/business/Vision.md

## Status
Approved

## Summary

HSK Learning là sản phẩm học tiếng Trung dành cho người Việt mới bắt đầu, cung cấp lộ trình
phát triển từ HSK 1 đến HSK 6 với trọng tâm từ vựng, ngữ pháp, nghe và phát âm. Sản phẩm
giúp người học ghi nhớ từ vựng bằng flip-card, hiểu nội dung qua giải thích tiếng Việt và
âm Hán–Việt, nhận biết lỗi phát âm thường gặp, đồng thời nhận bài học phù hợp với trình độ
và nhu cầu học tập. Tiến bộ được đánh giá qua mức độ hoàn thành, khả năng ghi nhớ dài hạn
và kết quả kiểm tra theo từng cấp HSK.

## Epics

### Approved learning-loop increment (2026-07-30)

The first HSK 1 increment operationalizes the epics with five multi-activity lessons: sentence-level
dialogue audio, Pinyin/translation controls, spaced-repetition flashcards, listening choice, sentence
ordering, local pronunciation recording/playback, per-lesson progress, daily streaks, a checkpoint
after five lessons, a personal vocabulary notebook, and focused review of wrong answers. This is an
implemented product increment, not an expansion beyond the approved HSK 1–6 scope.

### Epic-1: Lộ trình học HSK 1–6
- Priority: Must
- Vision goals: G-1, G-3
- Scope: Cung cấp một hành trình học có cấu trúc từ HSK 1 đến HSK 6 để người mới biết mình
  đang ở đâu, cần học gì tiếp theo và có thể duy trì tiến độ qua từng cấp.
- Future spec slug: hsk-learning-path

### Epic-2: Học và ôn từ vựng bằng flip-card
- Priority: Must
- Vision goals: G-2, G-4
- Scope: Cho phép người học tiếp cận và ôn tập từ vựng theo dạng flip-card, kết nối chữ Hán,
  pinyin, âm Hán–Việt, nghĩa tiếng Việt và ngữ cảnh sử dụng nhằm hỗ trợ ghi nhớ chủ động và
  duy trì kiến thức trong dài hạn.
- Future spec slug: vocabulary-flip-cards

### Epic-3: Năng lực ngữ pháp, nghe và phát âm
- Priority: Must
- Vision goals: G-3, G-4
- Scope: Giúp người học xây dựng đồng đều năng lực ngữ pháp, nghe và phát âm theo từng cấp
  HSK, với cách diễn giải phù hợp cho người Việt và chú trọng những lỗi phát âm thường gặp.
- Future spec slug: integrated-language-skills

### Epic-4: Bài học phù hợp với người học
- Priority: Should
- Vision goals: G-1, G-3
- Scope: Sử dụng AI để hỗ trợ tạo và điều chỉnh bài học dựa trên trình độ, tiến độ và điểm
  yếu của người học, đồng thời giữ nội dung trong phạm vi HSK và đáp ứng tiêu chuẩn chất
  lượng học tập.
- Future spec slug: adaptive-ai-lessons

### Epic-5: Đánh giá và theo dõi tiến bộ
- Priority: Should
- Vision goals: G-1, G-2, G-3
- Scope: Giúp người học nhận biết sự tiến bộ qua mức độ hoàn thành bài học, khả năng ghi nhớ
  từ vựng sau thời gian ôn tập và kết quả đánh giá trước và sau mỗi cấp HSK.
- Future spec slug: learning-progress

### Epic-6: Hỗ trợ học tập theo ngữ cảnh người Việt
- Priority: Could
- Vision goals: G-4
- Scope: Mở rộng chiều sâu của phần giải thích tiếng Việt, liên hệ Hán–Việt và hướng dẫn
  khắc phục lỗi học tiếng Trung đặc thù để giảm trở ngại cho người mới và tăng khả năng tự
  học.
- Future spec slug: vietnamese-learning-support

## Out of Scope (product-level)

- Phục vụ người học ngoài Việt Nam trong giai đoạn đầu.
- Nội dung ngoài phạm vi HSK 1–6.
- Thay thế giáo viên hoặc cam kết người học đỗ kỳ thi HSK.
- Mạng xã hội học tập hoặc sàn kết nối gia sư.

## Constraints

- Sản phẩm phải ưu tiên trải nghiệm và cách giải thích phù hợp với người Việt mới học tiếng
  Trung.
- Nội dung học tập phải bám sát phạm vi HSK 1–6 và cần được kiểm soát về độ chính xác,
  đặc biệt đối với nội dung do AI hỗ trợ tạo ra.
- Việc sử dụng AI phải cân nhắc quyền riêng tư của người học, chi phí vận hành, độ trễ,
  giới hạn sử dụng và tính liên tục của trải nghiệm khi dịch vụ bên ngoài không khả dụng.
- Các mục tiêu về tỷ lệ hoàn thành, ghi nhớ sau 30 ngày và cải thiện điểm kiểm tra phải có
  khả năng đo lường trong 6–12 tháng đầu.
