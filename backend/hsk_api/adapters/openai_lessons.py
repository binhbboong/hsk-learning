from typing import Any

from openai import OpenAI

from hsk_api.models.lesson import Lesson


class OpenAILessonGenerator:
    def __init__(
        self,
        *,
        client: Any,
        model: str,
        timeout_seconds: float,
    ) -> None:
        self._client = client
        self._model = model
        self._timeout_seconds = timeout_seconds

    @classmethod
    def from_api_key(
        cls,
        *,
        api_key: str,
        model: str,
        timeout_seconds: float,
    ) -> "OpenAILessonGenerator":
        return cls(
            client=OpenAI(api_key=api_key),
            model=model,
            timeout_seconds=timeout_seconds,
        )

    def generate(self, *, level: int, size: int) -> Lesson:
        response = self._client.responses.parse(
            model=self._model,
            instructions=(
                "Bạn là chuyên gia biên soạn bài học HSK cho người Việt mới bắt đầu. "
                "Chỉ tạo nội dung đúng cấp HSK được yêu cầu. Pinyin phải có dấu thanh, "
                "âm Hán–Việt và nghĩa phải bằng tiếng Việt, ví dụ phải tự nhiên và có "
                "bản dịch tiếng Việt. Không thêm trường ngoài schema."
            ),
            input=(
                f"Tạo một bài học từ vựng HSK {level} gồm đúng {size} thẻ. "
                "Mỗi thẻ phải có chữ Hán, pinyin, âm Hán–Việt, nghĩa tiếng Việt, "
                "một câu ví dụ tiếng Trung và bản dịch tiếng Việt."
            ),
            text_format=Lesson,
            timeout=self._timeout_seconds,
        )
        if response.output_parsed is None:
            raise ValueError("OpenAI did not return a structured lesson")
        return response.output_parsed
