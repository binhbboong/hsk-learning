# Wireframe: Checkpoint sau 5 bài
Supports journey: docs/ux/journeys/nguoi-moi-hoc-hsk-vong-hoc-hang-ngay.md

## Purpose

Kiểm tra ngắn các bài vừa học trước khi người học tiếp tục lộ trình.

## Layout

```text
+--------------------------------------------------+
| Checkpoint Bài 1-5 | câu n / tổng                 |
+--------------------------------------------------+
| Câu hỏi nghe / từ / sắp xếp câu                  |
| vùng trả lời                                     |
| [Gửi đáp án]                                     |
+--------------------------------------------------+
| Kết quả: điểm + câu sai + [Ôn câu sai]            |
+--------------------------------------------------+
```

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Phạm vi 5 bài | Cho biết lý do checkpoint | High |
| Câu hỏi hỗn hợp | Đo nhiều kỹ năng | High |
| Kết quả và lỗi sai | Biến kiểm tra thành đầu vào ôn | High |

## States

- Empty: chưa đủ 5 bài, quay về lộ trình.
- Loading: khung câu hỏi.
- Error: giữ câu trả lời hiện tại và cho thử lại.
- Populated: từng câu, kết quả và hành động ôn sai.
