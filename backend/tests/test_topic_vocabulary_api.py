from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from hsk_api.config import Settings
from hsk_api.main import create_app


class FakeTopicVocabularyGenerator:
    def __init__(
        self,
        *,
        invalid_session: bool = False,
        fail_recommendation: bool = False,
    ) -> None:
        self.recommendation_calls: list[dict] = []
        self.session_calls: list[dict] = []
        self.invalid_session = invalid_session
        self.fail_recommendation = fail_recommendation

    def recommend(self, **context):
        self.recommendation_calls.append(context)
        if self.fail_recommendation:
            raise Exception("provider rejected the configured key")
        suffix = len(self.recommendation_calls)
        return [
            {
                "id": f"ai-topic-{suffix}-{index}",
                "name_vi": f"Chủ đề AI {index}",
                "description_vi": "Từ vựng thực tế cho người mới.",
                "reason_vi": "Phù hợp với cấp HSK và lịch sử học của bạn.",
                "word_count": 10,
                "level": context["level"],
            }
            for index in range(1, 6)
        ]

    def generate_session(self, **context):
        self.session_calls.append(context)
        count = 9 if self.invalid_session else 10
        return {
            "id": f"{context['topic_id']}-session-1",
            "topic_id": context["topic_id"],
            "topic_name_vi": context["topic_name_vi"],
            "level": context["level"],
            "source": "ai",
            "words": [
                {
                    "id": f"词-{index}",
                    "hanzi": f"词{index}",
                    "pinyin": f"cí {index}",
                    "sino_vietnamese": "TỪ",
                    "meaning_vi": f"nghĩa {index}",
                    "example_zh": f"这是词{index}。",
                    "example_vi": f"Đây là từ {index}.",
                    "is_extension": False,
                }
                for index in range(1, count + 1)
            ],
        }


def register(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "display_name": "Người học chủ đề",
            "email": "topics@example.com",
            "password": "matkhau123",
        },
    )
    return {"Authorization": f"Bearer {response.json()['token']}"}


def test_topic_vocabulary_requires_authentication(tmp_path: Path) -> None:
    client = TestClient(create_app(database_path=tmp_path / "topics.sqlite3"))

    assert client.get("/api/v1/topic-vocabulary/recommendations").status_code == 401
    assert client.post(
        "/api/v1/topic-vocabulary/sessions",
        json={"topic_id": "greetings"},
    ).status_code == 401


def test_topic_vocabulary_uses_a_dedicated_generation_timeout(
    tmp_path: Path,
) -> None:
    settings = Settings(
        openai_api_key="test-key",
        openai_timeout_seconds=15,
        openai_topic_vocabulary_model="gpt-4.1-mini",
        openai_topic_vocabulary_timeout_seconds=60,
    )

    with (
        patch("hsk_api.main.get_settings", return_value=settings),
        patch(
            "hsk_api.main.OpenAITopicVocabularyGenerator.from_api_key",
        ) as factory,
    ):
        create_app(
            database_path=tmp_path / "topic-timeout.sqlite3",
            pronunciation_analyzer=None,
            speech_synthesizer=None,
            daily_path_generator=None,
        )

    factory.assert_called_once_with(
        api_key="test-key",
        model="gpt-4.1-mini",
        timeout_seconds=60,
    )


def test_returns_curated_recommendations_when_ai_is_unavailable(tmp_path: Path) -> None:
    client = TestClient(
        create_app(
            database_path=tmp_path / "fallback.sqlite3",
            topic_vocabulary_generator=None,
        )
    )
    headers = register(client)

    response = client.get(
        "/api/v1/topic-vocabulary/recommendations",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["source"] == "curated"
    assert len(response.json()["items"]) >= 5
    assert {item["id"] for item in response.json()["items"]}.issuperset(
        {"greetings", "family", "food", "travel", "shopping", "school", "work"}
    )
    assert all(item["word_count"] == 10 for item in response.json()["items"])


def test_refreshes_curated_recommendations_when_alternatives_exist(tmp_path: Path) -> None:
    client = TestClient(
        create_app(
            database_path=tmp_path / "fallback-refresh.sqlite3",
            topic_vocabulary_generator=None,
        )
    )
    headers = register(client)

    first = client.get(
        "/api/v1/topic-vocabulary/recommendations",
        headers=headers,
    ).json()
    refreshed = client.get(
        "/api/v1/topic-vocabulary/recommendations?refresh=true",
        headers=headers,
    ).json()

    assert len(first["items"]) >= 5
    assert len(refreshed["items"]) >= 5
    assert {item["id"] for item in first["items"]} != {
        item["id"] for item in refreshed["items"]
    }


def test_falls_back_when_the_ai_provider_rejects_the_request(
    tmp_path: Path,
    caplog,
) -> None:
    client = TestClient(
        create_app(
            database_path=tmp_path / "provider-error.sqlite3",
            topic_vocabulary_generator=FakeTopicVocabularyGenerator(
                fail_recommendation=True,
            ),
        )
    )
    headers = register(client)

    response = client.get(
        "/api/v1/topic-vocabulary/recommendations",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["source"] == "curated"
    assert "Topic recommendation generation failed" in caplog.text
    assert "provider rejected the configured key" in caplog.text


def test_refreshes_ai_recommendations_without_repeating_the_whole_list(
    tmp_path: Path,
) -> None:
    generator = FakeTopicVocabularyGenerator()
    client = TestClient(
        create_app(
            database_path=tmp_path / "refresh.sqlite3",
            topic_vocabulary_generator=generator,
        )
    )
    headers = register(client)

    first = client.get(
        "/api/v1/topic-vocabulary/recommendations",
        headers=headers,
    )
    cached = client.get(
        "/api/v1/topic-vocabulary/recommendations",
        headers=headers,
    )
    refreshed = client.get(
        "/api/v1/topic-vocabulary/recommendations?refresh=true",
        headers=headers,
    )

    assert first.status_code == 200
    assert first.json() == cached.json()
    assert len(generator.recommendation_calls) == 2
    assert refreshed.json()["items"] != first.json()["items"]
    assert generator.recommendation_calls[1]["previous_topic_ids"] == [
        item["id"] for item in first.json()["items"]
    ]


def test_creates_exactly_ten_words_and_reuses_the_persisted_session(
    tmp_path: Path,
) -> None:
    generator = FakeTopicVocabularyGenerator()
    client = TestClient(
        create_app(
            database_path=tmp_path / "session.sqlite3",
            topic_vocabulary_generator=generator,
        )
    )
    headers = register(client)
    topic = client.get(
        "/api/v1/topic-vocabulary/recommendations",
        headers=headers,
    ).json()["items"][0]

    first = client.post(
        "/api/v1/topic-vocabulary/sessions",
        json={"topic_id": topic["id"]},
        headers=headers,
    )
    second = client.post(
        "/api/v1/topic-vocabulary/sessions",
        json={"topic_id": topic["id"]},
        headers=headers,
    )

    assert first.status_code == 200
    assert first.json() == second.json()
    assert len(first.json()["words"]) == 10
    assert len({word["hanzi"] for word in first.json()["words"]}) == 10
    assert len(generator.session_calls) == 1


def test_invalid_ai_session_falls_back_to_curated_ten_words(tmp_path: Path) -> None:
    generator = FakeTopicVocabularyGenerator(invalid_session=True)
    client = TestClient(
        create_app(
            database_path=tmp_path / "quality.sqlite3",
            topic_vocabulary_generator=generator,
        )
    )
    headers = register(client)

    response = client.post(
        "/api/v1/topic-vocabulary/sessions",
        json={"topic_id": "greetings"},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["source"] == "curated"
    assert response.json()["topic_id"] == "greetings"
    assert len(response.json()["words"]) == 10
