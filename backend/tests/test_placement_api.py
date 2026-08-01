from pathlib import Path
from copy import deepcopy

from fastapi.testclient import TestClient

from hsk_api.main import create_app
from hsk_api.content.placement_test import placement_question
from hsk_api.content.learning_path import CHECKPOINT, LESSONS


class FakePronunciationAnalyzer:
    def analyze(self, **_kwargs):
        return {
            "verdict": "correct", "score": 86, "content_score": 90,
            "transcript": "你好", "feedback_vi": "Phát âm rõ.",
            "focus_vi": [], "syllables": [],
        }


class FakePlacementPathGenerator:
    def __init__(self, fail: bool = False) -> None:
        self.fail = fail

    def generate(self, **context):
        if self.fail:
            raise RuntimeError("AI unavailable")
        lessons = []
        for offset, source in enumerate(LESSONS):
            lesson = deepcopy(source.model_dump())
            number = context["start_number"] + offset
            lesson.update(id=f"hsk{context['level']}-lesson-{number}", number=number,
                          level=context["level"], title=f"HSK {context['level']} · {lesson['title']}",
                          goal=f"{lesson['goal']} · mục tiêu {number}")
            for key in ("dialogue", "vocabulary"):
                for index, item in enumerate(lesson[key]):
                    item["id"] = f"{lesson['id']}-{key}-{index}"
                    if key == "vocabulary":
                        item["hanzi"] = f"{item['hanzi']}{context['level']}"
            lesson["listening"]["id"] = f"{lesson['id']}-listening"
            lesson["sentence_order"]["id"] = f"{lesson['id']}-order"
            lessons.append(lesson)
        checkpoint = deepcopy(CHECKPOINT.model_dump())
        checkpoint.update(id=f"hsk{context['level']}-checkpoint-1-5",
                          lesson_ids=[lesson["id"] for lesson in lessons])
        return {"path_index": context["path_index"], "level": context["level"],
                "difficulty": context["difficulty"], "lessons": lessons,
                "checkpoint": checkpoint}


def register(client: TestClient, email: str = "placement@example.com") -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "display_name": "Người học xếp lớp",
            "email": email,
            "password": "matkhau123",
        },
    )
    return {"Authorization": f"Bearer {response.json()['token']}"}


def test_placement_requires_authentication(tmp_path: Path) -> None:
    client = TestClient(create_app(database_path=tmp_path / "placement-auth.sqlite3"))

    assert client.get("/api/v1/placement/status").status_code == 401
    assert client.post("/api/v1/placement/attempts").status_code == 401


def test_starts_and_resumes_without_exposing_the_answer(tmp_path: Path) -> None:
    client = TestClient(create_app(database_path=tmp_path / "placement-resume.sqlite3"))
    headers = register(client)

    started = client.post("/api/v1/placement/attempts", headers=headers)
    resumed = client.post("/api/v1/placement/attempts", headers=headers)

    assert started.status_code == 201
    assert resumed.status_code == 200
    assert resumed.json()["attempt_id"] == started.json()["attempt_id"]
    assert started.json()["question"]["skill"] == "vocabulary"
    assert started.json()["question"]["number"] == 1
    assert started.json()["question"]["total"] == 20
    assert len(started.json()["question"]["options"]) == 4
    assert "correct_option_id" not in started.json()["question"]


def test_answer_advances_and_persists_without_touching_learning_progress(
    tmp_path: Path,
) -> None:
    client = TestClient(create_app(database_path=tmp_path / "placement-answer.sqlite3"))
    headers = register(client)
    before = client.get("/api/v1/profile", headers=headers).json()
    attempt = client.post("/api/v1/placement/attempts", headers=headers).json()

    answered = client.post(
        f"/api/v1/placement/attempts/{attempt['attempt_id']}/answers",
        json={"option_id": attempt["question"]["options"][0]["id"]},
        headers=headers,
    )
    resumed = client.post("/api/v1/placement/attempts", headers=headers)
    after = client.get("/api/v1/profile", headers=headers).json()

    assert answered.status_code == 200
    assert answered.json()["question"]["number"] == 2
    assert resumed.json()["question"]["number"] == 2
    assert after == before


def test_can_skip_to_hsk_one_without_creating_learning_activity(tmp_path: Path) -> None:
    client = TestClient(create_app(database_path=tmp_path / "placement-skip.sqlite3"))
    headers = register(client)

    skipped = client.post("/api/v1/placement/skip", headers=headers)
    profile = client.get("/api/v1/profile", headers=headers).json()
    status = client.get("/api/v1/placement/status", headers=headers).json()

    assert skipped.status_code == 200
    assert skipped.json()["selected_level"] == 1
    assert profile["completedLessonIds"] == []
    assert profile["checkpointResults"] == []
    assert profile["activityEvents"] == []
    assert profile["startingLevel"] == 1
    assert status["can_take"] is True


def test_completes_twenty_adaptive_questions_and_locks_retake(tmp_path: Path) -> None:
    client = TestClient(create_app(
        database_path=tmp_path / "placement-complete.sqlite3",
        pronunciation_analyzer=FakePronunciationAnalyzer(),
    ))
    headers = register(client)
    attempt = client.post("/api/v1/placement/attempts", headers=headers).json()

    while attempt["status"] == "in_progress":
        question = attempt["question"]
        definition = placement_question(question["id"])
        assert definition is not None
        if question["skill"] == "pronunciation":
            response = client.post(
                f"/api/v1/placement/attempts/{attempt['attempt_id']}/pronunciation",
                files={"audio": ("voice.wav", b"RIFF-placement-audio", "audio/wav")},
                headers=headers,
            )
        else:
            response = client.post(
                f"/api/v1/placement/attempts/{attempt['attempt_id']}/answers",
                json={"option_id": definition.correct_option_id},
                headers=headers,
            )
        assert response.status_code == 200
        attempt = response.json()

    status = client.get("/api/v1/placement/status", headers=headers).json()

    assert attempt["result"]["recommended_level"] == 5
    assert len(attempt["result"]["skills"]) == 4
    assert sum(item["assessed"] for item in attempt["result"]["skills"]) == 20
    assert status["can_take"] is False
    assert status["retake_available_at"] is not None


def test_applies_selected_hsk_one_without_resetting_or_creating_progress(tmp_path: Path) -> None:
    client = TestClient(create_app(database_path=tmp_path / "placement-apply.sqlite3"))
    headers = register(client)

    response = client.post(
        "/api/v1/placement/selection",
        json={"selected_level": 1},
        headers=headers,
    )
    profile = client.get("/api/v1/profile", headers=headers).json()

    assert response.status_code == 200
    assert response.json() == {"selected_level": 1, "applied": True}
    assert profile["startingLevel"] == 1
    assert profile["completedLessonIds"] == []
    assert profile["activityEvents"] == []


def test_applies_higher_level_only_after_its_first_day_is_ready(tmp_path: Path) -> None:
    client = TestClient(create_app(
        database_path=tmp_path / "placement-hsk3.sqlite3",
        daily_path_generator=FakePlacementPathGenerator(),
    ))
    headers = register(client)

    selected = client.post(
        "/api/v1/placement/selection", json={"selected_level": 3}, headers=headers,
    )
    path = client.get("/api/v1/path", headers=headers).json()
    profile = client.get("/api/v1/profile", headers=headers).json()

    assert selected.status_code == 200
    assert profile["startingLevel"] == 3
    assert path["current_level"] == 3
    assert path["current_day_number"] == 1
    assert len(path["lessons"]) == 5
    assert path["days"][0]["level"] == 3
    assert all(lesson["id"].startswith("hsk3-") for lesson in path["lessons"])


def test_generation_failure_does_not_partially_apply_higher_level(tmp_path: Path) -> None:
    client = TestClient(create_app(
        database_path=tmp_path / "placement-hsk4-fail.sqlite3",
        daily_path_generator=FakePlacementPathGenerator(fail=True),
    ))
    headers = register(client)

    selected = client.post(
        "/api/v1/placement/selection", json={"selected_level": 4}, headers=headers,
    )
    profile = client.get("/api/v1/profile", headers=headers).json()
    path = client.get("/api/v1/path", headers=headers).json()

    assert selected.status_code == 503
    assert profile["startingLevel"] is None
    assert path["current_level"] == 1
    assert len(path["lessons"]) == 5
