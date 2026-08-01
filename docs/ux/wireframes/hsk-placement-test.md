# Wireframe: HSK Placement Test

Date: 2026-08-01
Related spec: `docs/specs/hsk-placement-test/Specification.md`

## 1. Điểm vào trên trang học

```text
┌──────────────────────────────────────────────────────────────┐
│ Xác định điểm bắt đầu phù hợp                                │
│ 20 câu · khoảng 12 phút · Từ vựng / Ngữ pháp / Nghe / Nói   │
│ [Kiểm tra đầu vào]                 [Bắt đầu HSK 1]            │
└──────────────────────────────────────────────────────────────┘
```

Chỉ ưu tiên thẻ này khi tài khoản chưa có tiến độ. Sau khi đã học, điểm vào chuyển vào phần cài
đặt/hồ sơ với nhãn “Đánh giá lại trình độ”.

## 2. Giới thiệu

```text
← Quay lại                                      Kiểm tra đầu vào

Tìm cấp HSK phù hợp với bạn
20 câu, khoảng 12 phút. Độ khó sẽ thay đổi theo câu trả lời.

[Từ vựng 5] [Ngữ pháp 5] [Nghe 5] [Phát âm 5]

Kết quả chỉ là gợi ý học tập. Bản thu không được lưu lại.

[Bắt đầu kiểm tra]
[Bỏ qua, học HSK 1]
```

## 3. Câu lựa chọn / nghe

```text
TỪ VỰNG                              Câu 3 / 20
████████░░░░░░░░░░░░

Chọn nghĩa đúng của “已经”

[A. đã]       [B. đang]
[C. sẽ]       [D. thường]

                                [Xác nhận]
```

Câu nghe thay phần câu hỏi bằng nút “Nghe câu” và cho phép phát lại; transcript chỉ xuất hiện ở
phần giải thích sau khi hoàn tất.

## 4. Câu phát âm

```text
PHÁT ÂM                              Câu 17 / 20
█████████████████░░░

Đọc câu sau:
你好，很高兴认识你。
nǐ hǎo, hěn gāoxìng rènshi nǐ.

[Nghe mẫu]  [Bắt đầu thu âm]
[▶ Nghe lại] [Thu lại] [Gửi phân tích]

Không thể dùng microphone? [Bỏ qua câu này]
```

## 5. Kết quả và chọn điểm bắt đầu

```text
Kết quả của bạn
Đề xuất: HSK 3                         Độ tin cậy: Khá

Từ vựng  HSK 3  ██████░░
Ngữ pháp HSK 2  █████░░░
Nghe      HSK 3  ██████░░
Phát âm   HSK 2  ████░░░░

Bạn hiểu tốt từ vựng quen thuộc; nên củng cố trật tự câu và thanh 3.
Đây là gợi ý học tập, không phải điểm thi HSK chính thức.

Điểm bắt đầu: [HSK 1] [HSK 2] [HSK 3✓] [HSK 4] [HSK 5] [HSK 6]
[Dùng cấp này và tạo Ngày 1]
[Về trang học]
```

Nếu tài khoản đã có tiến độ, vùng chọn cấp được thay bằng thông báo “Kết quả tham khảo; lộ trình
hiện tại của bạn được giữ nguyên”.

## Responsive và accessibility

- Desktop dùng tối đa 760 px cho vùng câu hỏi; mobile xếp lựa chọn một cột.
- Trạng thái chọn không chỉ phụ thuộc màu; có viền, dấu chọn và `aria-pressed`.
- Progress bar có nhãn đọc màn hình; mọi thao tác có thể dùng bàn phím.
- Nút thu âm luôn hiển thị trạng thái đang thu và thời lượng.
