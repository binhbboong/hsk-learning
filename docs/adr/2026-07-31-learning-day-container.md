# ADR: Dùng Ngày làm đơn vị trải nghiệm ngoài cùng

Date: 2026-07-31
Slug: learning-day-container
Status: Accepted
Related spec: docs/specs/daily-learning-days/Specification.md

## Context

Hệ thống đã tạo và lưu bất biến từng nhóm 5 bài cùng checkpoint, nhưng giao diện và tài liệu
gọi đơn vị này là “chặng”. Người học muốn nhìn lộ trình tự nhiên theo Ngày 1, Ngày 2… trong
khi khái niệm Bài và số bài liên tục vẫn giữ nguyên. “Ngày học” không được nhầm với ngày lịch,
vì người học có thể hoàn thành nhiều ngày học trong một ngày thực tế.

## Decision

Ngày là đơn vị trải nghiệm ngoài cùng, gồm đúng 5 Bài và một checkpoint. Hoàn thành đủ 5 Bài
và checkpoint của Ngày N mở ngay Ngày N+1. Ngày không mang ngày tháng và không ép người học
chờ sang hôm sau. `path_index` tiếp tục là định danh lưu trữ nội bộ tương ứng với số Ngày;
API tổng quan cung cấp metadata Ngày riêng để giao diện không phải tự suy luận cấu trúc.

## Consequences

Người học có mô hình tinh thần rõ ràng và vẫn có thể học nhanh hơn một ngày học mỗi ngày lịch.
Dữ liệu AI đã lưu và số Bài cũ không cần migration. API tổng quan lớn hơn vì trả thêm danh sách
Ngày, và mọi trạng thái hoàn thành/checkpoint phải được tính nhất quán từ hồ sơ học. “Chuỗi ngày”
tiếp tục chỉ phản ánh ngày lịch có hoạt động, độc lập với số Ngày học đã hoàn thành.
