# Wireframe: Trung tâm ôn tập
Supports journey: docs/ux/journeys/nguoi-moi-hoc-hsk-vong-hoc-hang-ngay.md

## Purpose

Gom thẻ SRS đến hạn và câu làm sai thành hai hàng đợi có lý do rõ ràng.

## Layout

```text
+--------------------------------------------------+
| Trung tâm ôn | số mục đến hạn                     |
+--------------------------------------------------+
| Tab: [Ôn ngắt quãng] [Câu làm sai]               |
| Thẻ/câu hiện tại                                 |
| [Xem đáp án] / [Chọn đáp án]                     |
| [Quên] [Khó] [Nhớ]                               |
+--------------------------------------------------+
| Tiến độ hàng đợi + hoàn thành                     |
+--------------------------------------------------+
```

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Hai loại hàng đợi | Phân biệt ôn theo lịch và ôn theo lỗi | High |
| Lý do xuất hiện | Giúp người học tin lịch ôn | Medium |
| Ba mức SRS | Lập lịch lần ôn tiếp theo | High |
| Xóa khỏi lỗi sai khi trả lời đúng | Cho thấy đã sửa được lỗi | High |

## States

- Empty: chúc mừng và quay về bài tiếp theo.
- Loading: khung thẻ/câu.
- Error: giữ hàng đợi local và cảnh báo nội dung thiếu.
- Populated: một mục mỗi lần với tiến độ.
