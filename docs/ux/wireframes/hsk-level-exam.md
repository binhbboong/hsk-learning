# Wireframe: Bài thi tổng kết HSK

## Purpose

Giúp người học hoàn thành bài đánh giá cuối cấp, hiểu kết quả và chuyển sang hành động phù hợp.

## Layout

### 1. Mở khóa bài thi

```text
+------------------------------------------------------------+
| ← Lộ trình                     Tổng kết HSK 2              |
+------------------------------------------------------------+
| Bạn đã sẵn sàng kiểm tra toàn cấp                          |
| 20 câu · Từ vựng / Ngữ pháp / Đọc / Nghe                  |
| Điều kiện đạt: tổng ≥80%, mỗi kỹ năng ≥60%                 |
|                                                            |
| [Bắt đầu bài thi]             [Ôn lại trước]               |
+------------------------------------------------------------+
```

### 2. Làm bài

```text
+------------------------------------------------------------+
| TỪ VỰNG · Câu 3/20                       08:42             |
| ███████-----------------------------------------           |
+------------------------------------------------------------+
| Chọn nghĩa đúng của ...                                   |
| [A ...]                         [B ...]                    |
| [C ...]                         [D ...]                    |
|                                                            |
| [Đánh dấu xem lại]              [Lưu và tiếp tục]          |
+------------------------------------------------------------+
| 1 ✓  2 ✓  3 ●  4 ?  5 ...  | [Nộp bài]                   |
+------------------------------------------------------------+
```

Phần nghe thay nội dung nguồn bằng nút “Nghe câu”. Transcript không xuất hiện khi đang thi.

### 3. Kết quả

```text
+------------------------------------------------------------+
| KẾT QUẢ HSK 2                                              |
| 17/20 · 85%                         ĐẠT                    |
|                                                            |
| Từ vựng  80% | Ngữ pháp 80% | Đọc 100% | Nghe 80%        |
|                                                            |
| Bạn đã sẵn sàng học HSK 3.                                |
| Đây là đánh giá học tập, không phải điểm thi chính thức.   |
|                                                            |
| [Tạo Ngày đầu tiên HSK 3]      [Xem lại lộ trình]          |
+------------------------------------------------------------+
```

Nếu chưa đạt, hành động chính là “Học củng cố”, hành động phụ là “Thi lại”. Nếu đạt HSK 6,
hành động chính là “Xem hành trình đã hoàn thành”.

## Key Elements

| Element | Purpose | Priority |
|---|---|---|
| Điều kiện mở/đạt | Đặt kỳ vọng trước khi bắt đầu | Cao |
| Tiến độ và phần thi | Giúp người học định hướng | Cao |
| 4 đáp án | Trả lời câu hiện tại | Cao |
| Đánh dấu xem lại | Quản lý câu chưa chắc | Trung bình |
| Bảng điều hướng câu | Xem câu đã trả lời/đánh dấu | Trung bình |
| Kết quả từng kỹ năng | Hiểu điểm mạnh/yếu | Cao |
| Hành động sau kết quả | Tiếp tục hoặc củng cố | Cao |

## States

- Empty: Chưa đủ điều kiện; hiển thị rõ Bài/checkpoint/ghi nhớ còn thiếu.
- Loading: Đang tải hoặc chuẩn bị đề, không cho bắt đầu hai lần.
- Error: Giữ nguyên quyền thi, thông báo tiếng Việt và có nút thử lại.
- Populated: Intro, runner hoặc kết quả theo trạng thái lượt thi đã lưu.
