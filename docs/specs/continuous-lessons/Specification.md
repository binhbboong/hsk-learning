# Specification: Học liên tiếp nhiều bài

> Một Ngày học gồm 5 Bài và checkpoint. “Học tiếp” có thể đi qua nhiều Ngày học trong cùng
> một ngày lịch; streak vẫn chỉ tăng một lần theo ngày lịch thực tế.

## Status

Approved

## Overview

Người học đã hoàn thành bài của ngày hôm nay cần được quyền chủ động học ngay bài tiếp theo, không bị hiểu rằng phải chờ sang ngày hôm sau. Luồng hoàn thành vẫn phải giữ một lối quay về lộ trình và giữ checkpoint sau mỗi 5 bài.

## User Scenarios

- Là người mới học HSK, tôi muốn bắt đầu bài kế tiếp ngay sau khi hoàn thành bài hiện tại để tiếp tục khi còn thời gian.
- Là người học muốn dừng, tôi muốn quay về lộ trình sau khi hoàn thành để xem tiến độ.

## Functional Requirements

- FR-1: Sau khi hoàn thành một bài chưa phải bài thứ 5, hệ thống MUST hiển thị xác nhận hoàn thành và hành động học bài kế tiếp.
- FR-2: Trạng thái hoàn thành MUST có hành động quay về lộ trình.
- FR-3: Hệ thống MUST cho phép hoàn thành nhiều bài trong cùng một ngày.
- FR-4: Việc học nhiều bài trong cùng ngày MUST NOT tăng chuỗi ngày nhiều lần.
- FR-5: Sau bài thứ 5, hành động tiếp theo MUST dẫn đến checkpoint thay vì bài thứ 6.
- FR-6: Tiến độ và từ vựng ôn tập MUST được ghi nhận trước khi người học chọn hành động tiếp theo.

## Out of Scope

- Thay đổi cách tính chuỗi ngày học.
- Mở bài ngoài nội dung hiện có.
- Thay đổi điều kiện mở checkpoint.

## Open Questions

Không có.

## Acceptance Criteria

- [ ] Hoàn thành Bài 1 hiển thị “Học tiếp Bài 2” và “Về lộ trình”.
- [ ] Chọn học tiếp mở đúng bài kế tiếp.
- [ ] Hoàn thành Bài 5 hiển thị hành động làm checkpoint.
- [ ] Hai bài hoàn thành cùng ngày vẫn chỉ ghi nhận một ngày trong streak.
