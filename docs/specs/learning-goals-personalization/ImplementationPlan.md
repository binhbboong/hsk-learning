# Implementation plan

- Mở rộng `LearningProfilePayload` bằng một object preferences được Pydantic kiểm tra.
- Dùng API profile hiện có để đồng bộ, tránh thêm bảng hoặc endpoint trùng lặp.
- Truyền preferences từ `DailyPathService` sang generator; OpenAI adapter đưa vào prompt như ưu tiên mềm.
- Thêm màn hình Angular `/learn/preferences` dùng repository đồng bộ hiện có và một thẻ vào dashboard.
- Kiểm thử model validation, generator context, service action và build.
