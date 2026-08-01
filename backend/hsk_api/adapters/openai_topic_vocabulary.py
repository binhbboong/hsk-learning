from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from hsk_api.adapters.openai_client import create_openai_client
from hsk_api.models.topic_vocabulary import (
    TopicRecommendation,
    TopicVocabularySession,
)


class TopicRecommendationList(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: list[TopicRecommendation] = Field(min_length=5, max_length=7)


class OpenAITopicVocabularyGenerator:
    def __init__(self, *, client: Any, model: str, timeout_seconds: float) -> None:
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
    ) -> "OpenAITopicVocabularyGenerator":
        return cls(
            client=create_openai_client(api_key, timeout_seconds),
            model=model,
            timeout_seconds=timeout_seconds,
        )

    def recommend(self, **context: Any) -> list[TopicRecommendation]:
        response = self._client.responses.parse(
            model=self._model,
            instructions=(
                "Bạn là chuyên gia HSK cho người Việt. Đề xuất 5 đến 7 chủ đề từ vựng "
                "thực tế, khác nhau, tên/mô tả/lý do bằng tiếng Việt. Mỗi chủ đề có đúng "
                "10 từ, không vượt cấp HSK yêu cầu. ID dùng kebab-case ASCII."
            ),
            input=(
                f"Cấp hiện tại HSK {context['level']}. "
                f"Không lặp toàn bộ các chủ đề gần nhất: {context['previous_topic_ids']}. "
                f"Các lỗi gần đây để cá nhân hóa: {context['mistakes']}."
            ),
            text_format=TopicRecommendationList,
            timeout=self._timeout_seconds,
        )
        if response.output_parsed is None:
            raise ValueError("OpenAI did not return topic recommendations")
        return response.output_parsed.items

    def generate_session(self, **context: Any) -> TopicVocabularySession:
        response = self._client.responses.parse(
            model=self._model,
            instructions=(
                "Bạn là biên soạn viên từ vựng HSK cho người Việt. Tạo đúng 10 từ duy nhất "
                "theo chủ đề và cấp được yêu cầu. Mỗi từ phải có chữ Hán, Pinyin có dấu, "
                "âm Hán–Việt, nghĩa Việt tự nhiên, ví dụ Trung ngắn và bản dịch Việt. "
                "ID từ phải là 'word:' cộng chữ Hán. Không thêm trường ngoài schema."
            ),
            input=(
                f"topic_id={context['topic_id']}; tên={context['topic_name_vi']}; "
                f"HSK {context['level']}; session id={context['topic_id']}-session-1; "
                "source phải là ai. Chỉ đánh dấu is_extension khi thật sự cần và vẫn dễ hiểu."
            ),
            text_format=TopicVocabularySession,
            timeout=self._timeout_seconds,
        )
        if response.output_parsed is None:
            raise ValueError("OpenAI did not return a topic vocabulary session")
        return response.output_parsed
