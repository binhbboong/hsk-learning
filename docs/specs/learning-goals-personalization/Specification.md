# Specification: Learning Goals Personalization

## Goal

Cho phép người học khai báo mục tiêu, thời lượng mỗi ngày và tối đa ba chủ đề ưa thích; dùng dữ liệu này để định hướng nội dung AI của các Ngày học tiếp theo mà không làm sai cấp độ HSK.

## Functional requirements

- FR-01: Người học có thể chọn một mục tiêu: giao tiếp, du lịch, công việc, thi HSK hoặc văn hóa.
- FR-02: Người học chọn 10, 20 hoặc 30 phút/ngày và tối đa ba chủ đề.
- FR-03: Cấu hình được lưu theo tài khoản và chỉnh sửa bất cứ lúc nào.
- FR-04: Dashboard hiển thị lối vào cấu hình và tóm tắt lựa chọn hiện tại.
- FR-05: Backend truyền mục tiêu/chủ đề vào lời nhắc tạo Ngày học AI; cấp HSK và chất lượng nội dung vẫn là ràng buộc cao nhất.
- FR-06: Người chưa cấu hình vẫn học được bằng hành vi mặc định hiện tại.

## Acceptance criteria

- Cấu hình tồn tại sau tải lại/đăng nhập thiết bị khác.
- Không thể gửi hơn ba chủ đề hoặc giá trị ngoài danh sách.
- Fake generator nhận đúng `learning_goal`, `daily_minutes`, `preferred_topics`.
- Lời nhắc OpenAI nói rõ chủ đề là ưu tiên mềm, không được vượt cấp HSK.
