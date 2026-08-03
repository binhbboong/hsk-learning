# Specification: Lộ trình hằng ngày do AI tạo

> Quyết định `2026-07-31-learning-day-container` chuẩn hóa tên gọi hướng người học:
> mỗi “chặng học hằng ngày” trong tài liệu này được hiển thị là Ngày 1, Ngày 2…;
> `path_index` chỉ còn là chi tiết lưu trữ nội bộ.
Related UX:
- `docs/ux/wireframes/learning-progress-dashboard.md`
- `docs/ux/wireframes/checkpoint-test.md`

## Status

Clarified

## Overview

Người học hiện dừng lại sau 5 bài HSK 1 vì hệ thống coi nhóm bài đầu tiên là toàn bộ lộ
trình. Tính năng này biến mỗi nhóm 5 bài thành một chặng học hằng ngày. Sau khi hoàn thành
5 bài và checkpoint của chặng hiện tại, người học nhận một chặng mới gồm 5 bài do AI tạo
phù hợp với trình độ và lịch sử học.

Các bài vẫn là đơn vị nội dung chính và được đánh số liên tục. Khái niệm “hằng ngày” chỉ
dùng để tổ chức lộ trình thành các chặng có quy mô vừa phải; hệ thống không được dừng vĩnh
viễn sau chặng đầu tiên. Độ khó phải tăng có kiểm soát trong từng cấp và toàn bộ hành trình
phải đưa người học tuần tự từ HSK 1 đến HSK 6.

## User Scenarios

- Là người mới học HSK, tôi muốn có 5 bài mới sau khi hoàn thành chặng hiện tại để tiếp tục
  học vào những ngày sau.
- Là người học đã có lỗi sai và dữ liệu ôn tập, tôi muốn bài mới phù hợp với tiến độ của mình
  để không quá dễ hoặc quá khó.
- Là người học quay lại sau khi đóng ứng dụng, tôi muốn thấy đúng chặng AI đã được tạo trước
  đó để nội dung không thay đổi.
- Là người học muốn xem lại kiến thức, tôi muốn mở lại các bài cũ mà không làm mất chặng đang
  học.
- Là người học theo đuổi HSK 1–6, tôi muốn biết mình đang ở cấp nào và vì sao được chuyển cấp
  để không gặp bài quá sức.

## Functional Requirements

- FR-1: Mỗi chặng học hằng ngày MUST gồm đúng 5 bài, một phiên 10 từ theo chủ đề và một checkpoint sau các bước đó.
- FR-2: Các bài MUST được đánh số liên tục giữa các chặng, ví dụ Bài 1–5, Bài 6–10 và
  Bài 11–15.
- FR-3: Mỗi bài AI MUST có hội thoại, từ vựng, bài nghe chọn đáp án, bài sắp xếp câu và bài
  luyện phát âm.
- FR-4: Nội dung AI MUST giải thích bằng tiếng Việt, có Pinyin đúng dấu và nêu hỗ trợ phù hợp
  cho người Việt khi nội dung có điểm phát âm dễ sai.
- FR-5: Chặng tiếp theo MUST chỉ được mở sau khi người học hoàn thành đủ 5 bài, phiên 10 từ theo
  chủ đề và checkpoint của chặng hiện tại.
- FR-6: Sau khi đủ điều kiện mở, hệ thống MUST tạo hoặc cung cấp một chặng 5 bài tiếp theo
  thay vì báo rằng toàn bộ lộ trình đã hoàn thành.
- FR-7: Hệ thống MUST lưu cố định mỗi chặng đã tạo cho người học; tải lại trang, đăng nhập lại
  hoặc đổi thiết bị MUST NOT tạo một bộ bài khác cho cùng chặng.
- FR-8: Việc yêu cầu lại chặng tiếp theo MUST NOT tạo bản sao hoặc làm thay đổi số thứ tự bài.
- FR-9: Bài mới MUST phù hợp với cấp HSK hiện tại và cân nhắc các bài đã hoàn thành, từ đã
  học, câu làm sai và kết quả checkpoint gần nhất.
- FR-10: Trong cùng một chặng, AI MUST NOT tạo hai bài có cùng mục tiêu học chính.
- FR-11: Chặng mới MUST NOT ghi đè nội dung, tiến độ, thẻ ôn, câu sai hoặc sổ từ của các chặng
  trước.
- FR-12: Dashboard MUST hiển thị chặng đang học, tổng số bài đã hoàn thành và hành động tiếp
  theo là bài kế tiếp hoặc checkpoint đang chờ.
- FR-13: Sau khi hoàn thành checkpoint, dashboard MUST hiển thị trạng thái đang chuẩn bị
  chặng mới và sau đó cho phép bắt đầu bài đầu tiên của chặng đó.
- FR-14: Nếu không thể tạo chặng mới, hệ thống MUST giữ nguyên toàn bộ tiến độ, giải thích lỗi
  bằng tiếng Việt và cho phép thử lại.
- FR-15: Người học MUST có thể mở lại bài của chặng cũ mà không thay đổi chặng hiện tại.
- FR-16: Mỗi checkpoint MUST ghi rõ phạm vi 5 bài tương ứng, ví dụ “Checkpoint Bài 6–10”.
- FR-17: Hoàn thành nhiều bài hoặc mở chặng mới trong cùng một ngày MUST NOT làm tăng streak
  nhiều hơn một ngày.
- FR-18: Nội dung AI MUST được kiểm tra đủ cấu trúc và phạm vi HSK trước khi hiển thị cho
  người học.
- FR-19: Mỗi bài MUST được gắn với đúng một cấp từ HSK 1 đến HSK 6.
- FR-20: Trong cùng một cấp HSK, độ khó của bài mới MUST tăng dần dựa trên lượng từ vựng,
  độ phức tạp ngữ pháp, độ dài hội thoại, tốc độ nghe và mức hỗ trợ Pinyin/bản dịch.
- FR-21: Bài mới MUST ưu tiên nội dung chưa thành thạo nhưng MAY ôn lại kiến thức tiền đề
  của cấp hiện tại khi dữ liệu ghi nhớ hoặc lỗi sai cho thấy cần củng cố.
- FR-22: Nội dung của một bài MUST NOT sử dụng kiến thức trọng tâm vượt quá cấp HSK hiện tại,
  trừ phần xem trước được ghi rõ và có giải thích.
- FR-23: Hệ thống MUST đưa người học qua các cấp theo đúng thứ tự HSK 1, HSK 2, HSK 3,
  HSK 4, HSK 5 và HSK 6.
- FR-24: Hệ thống MUST chỉ chuyển sang cấp HSK tiếp theo sau khi người học hoàn thành phạm vi
  nội dung của cấp hiện tại, đạt ít nhất 80% checkpoint, ít nhất 70% ghi nhớ từ vựng và đạt
  bài thi tổng kết cấp theo đặc tả `hsk-level-exams`.
- FR-25: Dashboard MUST hiển thị cấp HSK hiện tại, tiến độ trong cấp và mục tiêu cần đạt để
  chuyển cấp.
- FR-26: Khi chuyển cấp, chặng đầu tiên của cấp mới MUST bắt đầu ở độ khó nhập môn của cấp đó
  và duy trì các kiến thức tiền đề quan trọng từ cấp trước.
- FR-27: Sau khi hoàn thành HSK 6, hệ thống MUST hiển thị trạng thái hoàn thành toàn bộ lộ
  trình HSK 1–6 thay vì tạo nội dung ngoài HSK 6.
- FR-28: Việc AI tạo bài khó hơn MUST dựa trên bằng chứng tiến bộ; hệ thống MUST NOT tăng cấp
  chỉ vì người học đã mở hoặc bỏ qua bài.

## Out of Scope

- Cam kết số chặng cần thiết để đỗ kỳ thi HSK.
- Cam kết nội dung AI tương đương đề thi HSK chính thức.
- Thông báo đẩy hoặc lịch nhắc học cho ngày hôm sau.
- Cho người học chỉnh sửa trực tiếp nội dung bài do AI tạo.
- Chia sẻ lộ trình giữa nhiều người học hoặc xuất bản lộ trình cộng đồng.
- Thay đổi thuật toán ôn tập ngắt quãng hiện tại.

## Open Questions

Không còn câu hỏi chặn.

## Acceptance Criteria

- [ ] AC-1: Hoàn thành Bài 1–5 và checkpoint mở một chặng mới gồm Bài 6–10.
- [ ] AC-2: Chặng Bài 6–10 có đúng 5 bài, mỗi bài đủ năm nhóm nội dung bắt buộc.
- [ ] AC-3: Tải lại hoặc đăng nhập trên thiết bị khác vẫn trả về cùng nội dung Bài 6–10.
- [ ] AC-4: Yêu cầu chặng tiếp theo nhiều lần không tạo trùng Bài 6–10.
- [ ] AC-5: Dashboard sau checkpoint không còn báo hoàn thành toàn bộ lộ trình mà dẫn tới
  Bài 6.
- [ ] AC-6: Checkpoint tiếp theo hiển thị đúng phạm vi “Bài 6–10”.
- [ ] AC-7: Lỗi tạo nội dung giữ nguyên tiến độ và cung cấp hành động thử lại.
- [ ] AC-8: Bài AI sai cấu trúc hoặc ngoài phạm vi HSK không được hiển thị.
- [ ] AC-9: Hoàn thành nhiều bài trong cùng ngày chỉ ghi nhận một ngày streak.
- [ ] AC-10: Bài cũ vẫn có thể mở lại sau khi chặng mới được tạo.
- [ ] AC-11: Các bài trong một cấp tăng dần độ khó nhưng không đưa kiến thức trọng tâm ngoài
  cấp hiện tại vào bài thường.
- [ ] AC-12: Người học có checkpoint dưới 80% hoặc tỷ lệ ghi nhớ từ vựng dưới 70% tiếp tục
  nhận bài củng cố ở cấp hiện tại thay vì bị chuyển cấp.
- [ ] AC-13: Người học hoàn thành phạm vi HSK 1, đạt checkpoint từ 80%, ghi nhớ từ 70% và
  đạt bài thi tổng kết nhận chặng HSK 2 đầu tiên với độ khó nhập môn HSK 2.
- [ ] AC-14: Dashboard hiển thị đúng cấp hiện tại, tiến độ trong cấp và điều kiện chuyển cấp.
- [ ] AC-15: Sau HSK 6, hệ thống dừng ở trạng thái hoàn thành HSK 1–6 và không tạo bài HSK 7
  hoặc nội dung ngoài phạm vi.
