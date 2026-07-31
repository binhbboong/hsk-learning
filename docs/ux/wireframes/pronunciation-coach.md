# Wireframe: Phòng luyện phát âm
Supports journey: docs/ux/journeys/nguoi-moi-hoc-hsk-luyen-da-ky-nang.md

## Purpose

Giúp người Việt nghe mẫu, ghi âm, nghe lại và nhận hướng dẫn sửa thanh điệu cụ thể.

## Layout

```text
+--------------------------------------------------+
| Thoát | Phát âm HSK 1 | quyền microphone          |
+--------------------------------------------------+
| Cụm từ mẫu: chữ Hán / pinyin / đường thanh điệu  |
| [Nghe mẫu]                                       |
+--------------------------------------------------+
| [Bắt đầu ghi] / [Dừng ghi] / thời lượng           |
| [Nghe bản ghi] [Ghi lại]                         |
+--------------------------------------------------+
| Tự đánh giá thanh điệu                            |
| [Chưa giống] [Gần đúng] [Đã giống]               |
+--------------------------------------------------+
| Phản hồi: lỗi người Việt thường gặp + mẹo sửa     |
| [Hoàn thành]                                     |
+--------------------------------------------------+
```

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Mẫu chữ Hán và pinyin | Xác định chính xác âm đích | High |
| Audio mẫu | Cho người học một chuẩn so sánh | High |
| Ghi âm và nghe lại | Tạo vòng lặp tự quan sát | High |
| Hướng dẫn thanh điệu | Chỉ ra lỗi thường gặp của người Việt | High |
| Fallback không microphone | Không chặn việc học | Medium |

## States

- Empty: không có mẫu và quay về danh mục.
- Loading: chờ nội dung mẫu.
- Error: microphone/audio bị từ chối, chuyển sang chế độ nghe và tự luyện.
- Populated: mẫu, ghi âm, playback, tự đánh giá và phản hồi.
