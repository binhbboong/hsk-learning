# User Journey: Hoàn thành phiên học từ vựng đầu tiên

Persona: docs/business/personas/nguoi-moi-hoc-hsk.md

## Scenario

Người mới mở HSK Learning với mục tiêu bắt đầu HSK 1, học một nhóm từ bằng flip-card và
nhìn thấy kết quả để biết mình nên tiếp tục như thế nào.

## Steps

| # | Action | Touchpoint | Persona's goal at this step | Risk of drop-off |
|---|---|---|---|---|
| 1 | Mở sản phẩm và xem lộ trình | Trang tổng quan học tập | Hiểu điểm bắt đầu mà không phải tự cấu hình | Trung bình: quá nhiều lựa chọn gây bối rối |
| 2 | Bắt đầu bài HSK 1 được đề xuất | Tổng quan bài học | Biết mục tiêu và quy mô phiên học | Thấp: mô tả không rõ hoặc phiên quá dài |
| 3 | Xem và tự nhớ từng từ | Phiên flip-card | Liên kết chữ Hán với pinyin, Hán–Việt và nghĩa | Cao: nội dung quá khó hoặc thao tác không rõ |
| 4 | Đánh dấu nhớ/chưa nhớ | Phiên flip-card | Phản hồi nhanh để điều chỉnh lượt ôn | Trung bình: sợ đánh giá sai hoặc không hiểu tác dụng |
| 5 | Hoàn thành phiên học | Kết quả phiên học | Thấy tiến bộ và các từ cần ôn lại | Thấp: kết quả không đưa ra bước tiếp theo |
| 6 | Chọn ôn lại hoặc về lộ trình | Kết quả / tổng quan | Tiếp tục mà không mất tiến độ | Thấp: không lưu được kết quả |

## Emotional Arc

Sự không chắc chắn cao nhất ở lúc bắt đầu và khi gặp chữ Hán đầu tiên. Cảm giác kiểm soát
tăng khi flip-card cho phép tự kiểm tra trước khi xem đáp án; điểm hài lòng cao nhất là lúc
người học thấy số từ đã nhớ, từ cần ôn và một bước tiếp theo rõ ràng.

## Success Criteria

- Người học bắt đầu phiên HSK 1 trong không quá 3 hành động từ trang tổng quan.
- Người học hoàn thành một phiên 5 từ trong khoảng 5 phút mà không cần hiểu thuật ngữ kỹ thuật.
- Kết quả phân biệt rõ từ đã nhớ/chưa nhớ và cung cấp hành động ôn lại hoặc tiếp tục.
- Tiến độ của phiên hiện tại được duy trì trong thời gian sử dụng local.

## Candidate Screens

- Learning Dashboard
- Lesson Overview
- Flip-card Study
- Session Results
