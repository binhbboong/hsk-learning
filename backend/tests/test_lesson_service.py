from dataclasses import dataclass

import pytest

from hsk_api.content.default_lesson import DEFAULT_HSK1_LESSON
from hsk_api.models.lesson import Lesson
from hsk_api.services.lessons import LessonService


@dataclass
class FakeGenerator:
    result: object

    def generate(self, *, level: int, size: int) -> object:
        assert level == 1
        assert size == 5
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


def test_service_returns_valid_generated_lesson() -> None:
    generated = DEFAULT_HSK1_LESSON.model_copy(
        update={"id": "ai-hsk1", "title": "Bài học phù hợp"}
    )

    response = LessonService(generator=FakeGenerator(generated)).recommended(level=1, size=5)

    assert response.source == "ai"
    assert response.id == "ai-hsk1"


@pytest.mark.parametrize(
    "result",
    [
        TimeoutError("provider timed out"),
        RuntimeError("provider failed"),
        {"id": "invalid"},
        Lesson.model_construct(
            id="invalid-card-count",
            level=1,
            title="Sai",
            goal="Sai",
            estimated_minutes=5,
            cards=[],
        ),
    ],
)
def test_service_falls_back_for_provider_or_schema_failure(result: object) -> None:
    response = LessonService(generator=FakeGenerator(result)).recommended(level=1, size=5)

    assert response.source == "fallback"
    assert response.id == DEFAULT_HSK1_LESSON.id
    assert len(response.cards) == 5


def test_service_without_generator_uses_fallback() -> None:
    response = LessonService(generator=None).recommended(level=1, size=5)

    assert response.source == "fallback"
