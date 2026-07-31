# Wireframe: Danh mục kỹ năng HSK 1
Supports journey: docs/ux/journeys/nguoi-moi-hoc-hsk-luyen-da-ky-nang.md

## Purpose

Giúp người mới hiểu và chọn bài từ vựng, ngữ pháp, nghe hoặc phát âm tiếp theo.

## Layout

```text
+--------------------------------------------------+
| Header: HSK Learning / HSK 1 / tiến độ            |
+--------------------------------------------------+
| Tiêu đề: Hôm nay bạn muốn luyện gì?               |
| Mô tả ngắn về phiên học 5-10 phút                 |
+--------------------------------------------------+
| [Từ vựng] [Ngữ pháp] [Nghe hiểu] [Phát âm]       |
| mục tiêu    mục tiêu    mục tiêu      mục tiêu    |
| trạng thái  hành động   hành động     hành động   |
+--------------------------------------------------+
| Lộ trình HSK 1 -> HSK 6                           |
+--------------------------------------------------+
```

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Nhóm thẻ kỹ năng | Hiển thị toàn bộ lựa chọn học trong một nơi | High |
| Mục tiêu và thời lượng | Giúp người mới chọn với kỳ vọng rõ ràng | High |
| Trạng thái hoàn thành | Tạo cảm giác tiến bộ | Medium |
| Lộ trình cấp độ | Giữ ngữ cảnh HSK 1–6 | Medium |

## States

- Empty: giải thích chưa có bài cho cấp này.
- Loading: thẻ khung giữ nguyên cấu trúc trang.
- Error: thông báo tiếng Việt và hành động thử lại.
- Populated: bốn thẻ kỹ năng với hành động riêng.
