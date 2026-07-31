# Wireframe: Session Results

Supports journey: docs/ux/journeys/nguoi-moi-hoc-hsk-hoc-tu-vung-dau-tien.md

## Purpose

Cho người học thấy kết quả phiên học và chọn bước tiếp theo rõ ràng.

## Layout

```text
+------------------------------------------------------+
| Header: HSK Learning · Hoàn thành                    |
+------------------------------------------------------+
| Main                                                  |
|  Bạn đã hoàn thành 5 thẻ                              |
|  [3 đã nhớ] [2 cần ôn]                                |
|                                                       |
|  Từ cần ôn: danh sách ngắn                            |
|                                                       |
|  [Ôn lại từ chưa nhớ]        [Về lộ trình]            |
+------------------------------------------------------+
```

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Tóm tắt hoàn thành | Tạo cảm giác tiến bộ | High |
| Số đã nhớ/cần ôn | Làm kết quả dễ hiểu | High |
| Danh sách cần ôn | Cho biết chính xác điểm yếu | Medium |
| Ôn lại | Củng cố từ chưa nhớ | High |
| Về lộ trình | Tiếp tục hành trình rộng hơn | Medium |

## States

- Empty: Không có kết quả; hướng người học quay lại lộ trình.
- Loading: Báo đang tổng hợp kết quả.
- Error: Báo chưa thể lưu/tổng hợp nhưng không làm mất kết quả phiên trong bộ nhớ.
- Populated: Hiển thị tóm tắt, từ cần ôn và hai hành động tiếp theo.
