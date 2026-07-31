# Wireframe: Flip-card Study

Supports journey: docs/ux/journeys/nguoi-moi-hoc-hsk-hoc-tu-vung-dau-tien.md

## Purpose

Cho người học chủ động nhớ lại một từ trước khi xem đáp án và tự đánh giá mức độ ghi nhớ.

## Layout

```text
+------------------------------------------------------+
| Header: [Thoát]  Bài HSK 1               2 / 5       |
| Progress: [========----------------]                  |
+------------------------------------------------------+
| Main                                                  |
|  +------------------------------------------------+  |
|  | Mặt trước: chữ Hán                            |  |
|  | Gợi ý: phát âm / câu hỏi ngắn                 |  |
|  |                                                |  |
|  | [Lật thẻ]                                      |  |
|  +------------------------------------------------+  |
|                                                       |
|  Sau khi lật: pinyin · Hán–Việt · nghĩa · ví dụ      |
|  [Chưa nhớ]                              [Đã nhớ]     |
+------------------------------------------------------+
```

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Chỉ báo tiến độ | Giúp phiên học có giới hạn rõ | High |
| Nội dung mặt trước | Kích hoạt nhớ chủ động | High |
| Lật thẻ | Cho người học kiểm tra câu trả lời | High |
| Pinyin/Hán–Việt/nghĩa/ví dụ | Giải thích từ theo ngữ cảnh người Việt | High |
| Nhớ/chưa nhớ | Ghi phản hồi để tính kết quả và ôn lại | High |
| Thoát | Cho phép rời phiên có chủ đích | Medium |

## States

- Empty: Báo bài chưa có thẻ và cho phép quay lại.
- Loading: Hiển thị vùng thẻ ổn định và báo đang tải từ tiếp theo.
- Error: Giữ tiến độ hiện tại, cho phép thử lại hoặc quay về bài học.
- Populated: Hiển thị mặt trước; sau khi lật mới hiện đáp án và hai lựa chọn đánh giá.
