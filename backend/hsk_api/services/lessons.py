from dataclasses import dataclass

from hsk_api.adapters.base import LessonGenerator
from hsk_api.adapters.openai_lessons import OpenAILessonGenerator
from hsk_api.config import get_settings
from hsk_api.content.default_lesson import DEFAULT_HSK1_LESSON
from hsk_api.models.lesson import Lesson, LessonResponse


@dataclass
class LessonService:
    generator: LessonGenerator | None = None

    def recommended(self, *, level: int, size: int) -> LessonResponse:
        if self.generator is not None:
            try:
                generated = Lesson.model_validate(
                    self.generator.generate(level=level, size=size)
                )
                return LessonResponse(**generated.model_dump(), source="ai")
            except Exception:
                pass

        return LessonResponse(**DEFAULT_HSK1_LESSON.model_dump(), source="fallback")


def create_default_service() -> LessonService:
    settings = get_settings()
    api_key = (
        settings.openai_api_key.get_secret_value().strip()
        if settings.openai_api_key else ""
    )
    if not api_key:
        return LessonService()

    return LessonService(
        generator=OpenAILessonGenerator.from_api_key(
            api_key=api_key,
            model=settings.openai_model,
            timeout_seconds=settings.openai_timeout_seconds,
        )
    )


_default_service = create_default_service()


def get_recommended_lesson() -> LessonResponse:
    return _default_service.recommended(level=1, size=5)
