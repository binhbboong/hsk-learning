from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_skill_catalog_lists_four_hsk1_learning_modes() -> None:
    response = client.get("/api/v1/skills", params={"level": 1})

    assert response.status_code == 200
    payload = response.json()
    assert payload["level"] == 1
    assert [item["kind"] for item in payload["items"]] == [
        "vocabulary",
        "grammar",
        "listening",
        "pronunciation",
    ]
    assert all(item["title"] and item["goal"] for item in payload["items"])
    assert all(3 <= item["estimated_minutes"] <= 10 for item in payload["items"])


def test_grammar_lesson_contains_pattern_examples_and_two_questions() -> None:
    response = client.get("/api/v1/skills/grammar", params={"level": 1})

    assert response.status_code == 200
    lesson = response.json()
    assert lesson["kind"] == "grammar"
    assert lesson["pattern"] == "A + 是 + B"
    assert len(lesson["examples"]) >= 2
    assert len(lesson["questions"]) >= 2
    assert all(example["hanzi"] and example["pinyin"] and example["meaning_vi"] for example in lesson["examples"])
    assert all(question["correct_option_id"] in {option["id"] for option in question["options"]} for question in lesson["questions"])


def test_listening_lesson_has_hidden_transcript_content_and_answer() -> None:
    response = client.get("/api/v1/skills/listening", params={"level": 1})

    assert response.status_code == 200
    lesson = response.json()
    assert lesson["kind"] == "listening"
    assert lesson["utterance_zh"] == "你好，我是王明。"
    assert lesson["pinyin"]
    assert lesson["meaning_vi"]
    assert lesson["correct_option_id"] in {option["id"] for option in lesson["options"]}


def test_pronunciation_lesson_has_vietnamese_specific_tone_guidance() -> None:
    response = client.get("/api/v1/skills/pronunciation", params={"level": 1})

    assert response.status_code == 200
    lesson = response.json()
    assert lesson["kind"] == "pronunciation"
    assert lesson["hanzi"] == "你好"
    assert lesson["pinyin"] == "nǐ hǎo"
    assert len(lesson["tone_path"]) == 2
    assert "người việt" in lesson["common_mistake_vi"].lower()
    assert lesson["correction_tip_vi"]


def test_skills_reject_levels_outside_current_hsk1_scope() -> None:
    assert client.get("/api/v1/skills", params={"level": 2}).status_code == 422
    assert client.get("/api/v1/skills/grammar", params={"level": 6}).status_code == 422
