# Wireframe: Học từ vựng theo chủ đề

Supports journey: nhu cầu học từ vựng riêng theo chủ đề do người học trực tiếp yêu cầu.

## Purpose

Giúp người học chọn một chủ đề AI đề xuất, học 10 từ bằng flipcard và xác nhận khả năng nhớ bằng
trắc nghiệm 4 đáp án trong một luồng ngắn, có thể tiếp tục sau khi tải lại.

## Layout

### Trạng thái chọn chủ đề

```text
+----------------------------------------------------------+
| ← Lộ trình     Từ vựng theo chủ đề       [Đề xuất mới]  |
+----------------------------------------------------------+
| HSK hiện tại | Giải thích cách AI chọn chủ đề            |
+----------------------------------------------------------+
| Chủ đề đề xuất                                            |
| +----------------------+ +----------------------+         |
| | Tên + mô tả          | | Tên + mô tả          |         |
| | Vì sao phù hợp       | | Vì sao phù hợp       |         |
| | tiến độ / 10 từ      | | tiến độ / 10 từ      |         |
| | [Bắt đầu/Tiếp tục]   | | [Bắt đầu/Tiếp tục]   |         |
| +----------------------+ +----------------------+         |
| ... tối thiểu 5 chủ đề                                    |
+----------------------------------------------------------+
```

### Trạng thái flipcard

```text
+----------------------------------------------------------+
| ← Chủ đề | Tên chủ đề                    Thẻ 3 / 10       |
+----------------------------------------------------------+
| [Thanh tiến độ]                                           |
| +------------------------------------------------------+ |
| |                     汉字                              | |
| |                 [Nghe từ]                            | |
| |                                                      | |
| |                  [Lật thẻ]                           | |
| +------------------------------------------------------+ |
| Mặt sau: Pinyin · Hán–Việt · nghĩa · ví dụ/ dịch         |
|          [Nghe từ] [Nghe câu]             [Từ tiếp theo] |
+----------------------------------------------------------+
```

### Trạng thái nhớ chủ động

```text
+----------------------------------------------------------+
| Tên chủ đề                         Câu 4 / 10             |
+----------------------------------------------------------+
| Chọn nghĩa đúng của:                 汉字                 |
| [Đáp án A] [Đáp án B] [Đáp án C] [Đáp án D]              |
| Phản hồi đúng/sai + nghĩa đúng                            |
| Đúng: tự chuyển ngắn | Sai: [Tiếp tục]                   |
+----------------------------------------------------------+
```

### Trạng thái hoàn thành

```text
+----------------------------------------------------------+
| Hoàn thành phiên: 10 từ | số từ nhớ đúng | tỷ lệ          |
| Các từ đã được đưa vào lịch ôn chung                     |
| [Học chủ đề khác] [Ôn từ đến hạn]                        |
+----------------------------------------------------------+
```

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Danh sách chủ đề + lý do | Giúp người mới quyết định nhanh và hiểu tính cá nhân hóa | High |
| Nút bắt đầu/tiếp tục | Vào đúng phiên mới hoặc vị trí đang dở | High |
| Flipcard một từ | Tập trung chú ý và buộc nhớ trước khi lật | High |
| Tiến độ 10 từ | Giữ kỳ vọng phiên ngắn và rõ ràng | High |
| Bốn đáp án | Kiểm tra nhớ chủ động sau lượt xem | High |
| Phản hồi đúng/sai | Củng cố nghĩa đúng và điều khiển nhịp chuyển từ | High |
| Đề xuất mới | Cho phép đổi danh sách mà không nhập chủ đề tự do | Medium |
| Âm thanh từ/câu | Kết nối chữ, nghĩa và phát âm | Medium |
| Kết quả phiên | Xác nhận hoàn thành và gợi ý hành động tiếp theo | Medium |

## States

- Empty: thông báo chưa có chủ đề phù hợp, cho thử đề xuất mới và quay lại lộ trình.
- Loading: giữ tiêu đề, hiển thị thông báo đang chuẩn bị đề xuất hoặc phiên 10 từ; khóa CTA lặp.
- Error: giải thích ngắn, cho thử lại; nếu có fallback thì ghi rõ đang dùng chủ đề đã kiểm duyệt.
- Populated: hiển thị tối thiểu 5 chủ đề với tiến độ và CTA tương ứng.
- Studying: khóa đổi chủ đề vô tình, lưu vị trí sau mỗi bước và cho quay về danh mục.
- Completed: hiển thị kết quả 10 từ, xác nhận SRS/streak và hai hành động tiếp theo.
- Exhausted: thông báo đã học hết nội dung hiện có của chủ đề, cho chọn chủ đề khác hoặc ôn lại.

## Interaction Rules

- Chỉ sau khi lật thẻ mới hiện nút sang từ tiếp theo.
- Sau thẻ thứ 10, chuyển sang lượt trắc nghiệm; không bỏ qua lượt xem.
- Chọn đúng: hiện phản hồi ngắn rồi tự chuyển đúng một lần.
- Chọn sai: giữ nguyên phản hồi và chỉ chuyển khi người học bấm `Tiếp tục`.
- Tải lại trang khôi phục đúng phase, index và câu trả lời đã ghi trong profile.
