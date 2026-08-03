# ADR: Đưa phiên từ vựng theo chủ đề vào điều kiện hoàn thành Ngày

Date: 2026-08-03
Slug: mandatory-daily-topic-vocabulary
Status: Accepted
Related spec: docs/specs/mandatory-daily-topic-vocabulary/Specification.md

## Context

Một Ngày hiện gồm 5 Bài và checkpoint, còn phiên 10 từ theo chủ đề là hoạt động bổ trợ độc lập.
Người học muốn việc xây vốn từ theo ngữ cảnh trở thành một phần nhất quán của mọi Ngày thay vì
một công cụ có thể bỏ qua. Quy tắc cũ vì vậy không còn phản ánh lộ trình mong muốn.

## Decision

Mỗi Ngày bắt buộc có một phiên 10 từ theo chủ đề do người học chọn từ danh sách AI đề xuất hoặc
danh mục dự phòng. Sau 5 Bài, hành động tiếp theo là hoàn thành phiên chủ đề nếu Ngày đó chưa có
phiên hoàn thành. Checkpoint chỉ được mở sau khi cả 5 Bài và phiên chủ đề đã hoàn thành. Ngày kế
tiếp chỉ được mở sau checkpoint như trước.

Các phiên chủ đề đã hoàn thành được phân bổ tuần tự cho các Ngày để giữ tương thích với hồ sơ hiện
có; một phiên chỉ đáp ứng tối đa một Ngày. Phiên vẫn không được tính là một Bài và không tự thay đổi
cấp HSK.

## Consequences

- Mỗi Ngày có nhịp học rõ ràng: 5 Bài, 10 từ theo chủ đề, checkpoint.
- Dashboard và API phải biểu diễn riêng trạng thái phiên chủ đề bắt buộc.
- Điều kiện tạo Ngày kế tiếp phải kiểm tra cả tiến độ phiên chủ đề, không chỉ 5 Bài và checkpoint.
- Người học cũ được ghi nhận các phiên chủ đề đã hoàn thành theo thứ tự, tránh buộc học lại dữ liệu cũ.
- Khu học chủ đề vẫn có thể truy cập độc lập; các phiên hoàn thành thêm sẽ được dùng cho Ngày kế tiếp
  theo thứ tự.
