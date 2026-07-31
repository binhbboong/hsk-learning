from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_learning_path_lists_five_hsk1_lessons() -> None:
    response = client.get("/api/v1/path", params={"level": 1})

    assert response.status_code == 200
    payload = response.json()
    assert payload["level"] == 1
    assert len(payload["lessons"]) == 5
    assert [lesson["number"] for lesson in payload["lessons"]] == [1, 2, 3, 4, 5]


def test_multi_activity_lesson_contains_dialogue_listening_reorder_and_words() -> None:
    response = client.get("/api/v1/path/lessons/1")

    assert response.status_code == 200
    lesson = response.json()
    assert lesson["id"] == "hsk1-lesson-1"
    assert len(lesson["dialogue"]) >= 2
    assert all(line["audio_text"] and line["pinyin"] and line["translation_vi"] for line in lesson["dialogue"])
    assert lesson["listening"]["correct_option_id"] in {
        option["id"] for option in lesson["listening"]["options"]
    }
    assert sorted(lesson["sentence_order"]["tokens"]) == sorted(
        lesson["sentence_order"]["correct_tokens"]
    )
    assert len(lesson["vocabulary"]) >= 2


def test_checkpoint_covers_listening_vocabulary_and_sentence_order() -> None:
    response = client.get("/api/v1/path/checkpoint")

    assert response.status_code == 200
    checkpoint = response.json()
    assert checkpoint["id"] == "hsk1-checkpoint-1-5"
    assert [question["kind"] for question in checkpoint["questions"]] == [
        "listening",
        "vocabulary",
        "sentence-order",
    ]


def test_invalid_or_unavailable_lesson_numbers_are_rejected() -> None:
    assert client.get("/api/v1/path/lessons/0").status_code == 422
    assert client.get("/api/v1/path/lessons/6").status_code == 404
