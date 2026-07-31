from dataclasses import dataclass

from hsk_api.adapters.openai_lessons import OpenAILessonGenerator
from hsk_api.content.default_lesson import DEFAULT_HSK1_LESSON
from hsk_api.models.lesson import Lesson


@dataclass
class FakeParsedResponse:
    output_parsed: Lesson | None


class FakeResponses:
    def __init__(self, parsed: Lesson | None) -> None:
        self.parsed = parsed
        self.kwargs: dict[str, object] | None = None

    def parse(self, **kwargs: object) -> FakeParsedResponse:
        self.kwargs = kwargs
        return FakeParsedResponse(self.parsed)


class FakeClient:
    def __init__(self, parsed: Lesson | None) -> None:
        self.responses = FakeResponses(parsed)


def test_openai_adapter_requests_structured_lesson() -> None:
    client = FakeClient(DEFAULT_HSK1_LESSON)
    adapter = OpenAILessonGenerator(
        client=client,
        model="configured-model",
        timeout_seconds=7.0,
    )

    lesson = adapter.generate(level=1, size=5)

    assert lesson == DEFAULT_HSK1_LESSON
    assert client.responses.kwargs is not None
    assert client.responses.kwargs["model"] == "configured-model"
    assert client.responses.kwargs["text_format"] is Lesson
    assert client.responses.kwargs["timeout"] == 7.0
    assert "người Việt" in str(client.responses.kwargs["instructions"])


def test_openai_adapter_rejects_empty_parsed_output() -> None:
    adapter = OpenAILessonGenerator(
        client=FakeClient(None),
        model="configured-model",
        timeout_seconds=7.0,
    )

    try:
        adapter.generate(level=1, size=5)
    except ValueError as error:
        assert "structured lesson" in str(error)
    else:
        raise AssertionError("Expected missing structured output to fail")
