from typing import Any

from hsk_api.adapters.openai_client import create_openai_client
from hsk_api.models.learning_loop import DailyPathBundle


class OpenAIDailyPathGenerator:
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
        self.last_usage: dict[str, int] = {}

    @classmethod
    def from_api_key(
        cls,
        *,
        api_key: str,
        model: str,
        timeout_seconds: float,
    ) -> "OpenAIDailyPathGenerator":
        return cls(
            client=create_openai_client(api_key, timeout_seconds),
            model=model,
            timeout_seconds=timeout_seconds,
        )

    def generate(self, **context: Any) -> DailyPathBundle:
        start = int(context["start_number"])
        end = start + 4
        level = int(context["level"])
        response = self._client.responses.parse(
            model=self._model,
            instructions=(
                "Bạn là chuyên gia xây lộ trình HSK cho người Việt. "
                "Tạo đúng 5 bài đa kỹ năng và 1 checkpoint theo schema. "
                "Mỗi bài phải có hội thoại tự nhiên, Pinyin có dấu, bản dịch và giải thích "
                "tiếng Việt, từ vựng, nghe chọn đáp án, sắp xếp câu và phát âm. "
                "Không dùng kiến thức trọng tâm vượt cấp HSK yêu cầu. "
                "Mục tiêu của 5 bài phải khác nhau. Không thêm trường ngoài schema."
            ),
            input=(
                f"Tạo path_index={context['path_index']}, HSK {level}, "
                f"difficulty={context['difficulty']}, gồm Bài {start} đến Bài {end}. "
                f"ID bài phải theo mẫu hsk{level}-lesson-<number>. "
                f"Checkpoint có ID hsk{level}-checkpoint-{start}-{end}, tiêu đề "
                f"'Checkpoint Bài {start}–{end}' và lesson_ids khớp đúng 5 bài. "
                f"Checkpoint gần nhất={context['checkpoint_rate']:.2f}; "
                f"ghi nhớ từ vựng={context['retention_rate']:.2f}. "
                f"Không lặp mục tiêu gần đây: {context['previous_titles']}. "
                f"Điểm yếu cần cân nhắc: {context['mistake_prompts']}."
            ),
            text_format=DailyPathBundle,
            timeout=self._timeout_seconds,
        )
        if response.output_parsed is None:
            raise ValueError("OpenAI did not return a structured daily path")
        usage = getattr(response, "usage", None)
        self.last_usage = {
            "input_tokens": int(getattr(usage, "input_tokens", 0) or 0),
            "output_tokens": int(getattr(usage, "output_tokens", 0) or 0),
        }
        return response.output_parsed
