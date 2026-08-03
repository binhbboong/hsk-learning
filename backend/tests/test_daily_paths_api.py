from copy import deepcopy
from pathlib import Path

from fastapi.testclient import TestClient

from hsk_api.content.learning_path import CHECKPOINT, LESSONS
from hsk_api.main import create_app


class FakeDailyPathGenerator:
    def __init__(self, *, fail: bool = False) -> None:
        self.calls: list[dict] = []
        self.fail = fail

    def generate(self, **context):
        self.calls.append(context)
        if self.fail:
            raise RuntimeError("AI unavailable")
        start = context["start_number"]
        level = context["level"]
        lessons = []
        for offset, source in enumerate(LESSONS):
            number = start + offset
            lesson = deepcopy(source.model_dump())
            lesson.update(
                id=f"hsk{level}-lesson-{number}",
                number=number,
                level=level,
                title=f"HSK {level} · {lesson['title']}",
                goal=f"{lesson['goal']} · mục tiêu {number}",
            )
            for key in ("dialogue", "vocabulary"):
                for item_index, item in enumerate(lesson[key], 1):
                    item["id"] = f"{lesson['id']}-{key}-{item_index}"
                    if key == "vocabulary":
                        item["hanzi"] = f"{item['hanzi']}{number}"
            lesson["listening"]["id"] = f"{lesson['id']}-listening"
            lesson["sentence_order"]["id"] = f"{lesson['id']}-order"
            lessons.append(lesson)
        checkpoint = deepcopy(CHECKPOINT.model_dump())
        checkpoint.update(
            id=f"hsk{level}-checkpoint-{start}-{start + 4}",
            title=f"Checkpoint Bài {start}–{start + 4}",
            lesson_ids=[lesson["id"] for lesson in lessons],
        )
        return {
            "path_index": context["path_index"],
            "level": level,
            "difficulty": context["difficulty"],
            "lessons": lessons,
            "checkpoint": checkpoint,
        }


def register(client: TestClient) -> tuple[str, dict[str, str]]:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "display_name": "Người học AI",
            "email": "ai-path@example.com",
            "password": "matkhau123",
        },
    )
    token = response.json()["token"]
    return token, {"Authorization": f"Bearer {token}"}


def ready_profile(*, score: int = 3, total: int = 3, remembered: int = 8) -> dict:
    cards = []
    for index in range(10):
        cards.append(
            {
                "id": f"word-{index}",
                "hanzi": "你",
                "pinyin": "nǐ",
                "meaningVi": "bạn",
                "sourceLessonId": f"hsk1-lesson-{(index // 2) + 1}",
                "repetitions": 1 if index < remembered else 0,
                "intervalDays": 7,
                "dueDate": "2026-08-07",
            }
        )
    return {
        "version": 1,
        "completedLessonIds": [f"hsk1-lesson-{number}" for number in range(1, 6)],
        "streak": {"current": 1, "longest": 1, "lastActiveDate": "2026-07-31"},
        "reviewCards": cards,
        "mistakes": [],
        "notebook": [],
        "checkpointResults": [
            {
                "checkpointId": "hsk1-checkpoint-1-5",
                "score": score,
                "total": total,
                "completedAt": "2026-07-31",
            }
        ],
        "topicVocabularyProgress": [
            {
                "topicId": "daily-topic-1",
                "sessionId": "daily-topic-1-session-1",
                "phase": "completed",
                "cardIndex": 10,
                "quizIndex": 10,
                "learnedWordIds": [f"topic-word-{index}" for index in range(10)],
                "correctWordIds": [f"topic-word-{index}" for index in range(8)],
                "updatedAt": "2026-07-31T12:00:00Z",
            }
        ],
    }


def complete_generated_day(profile: dict, bundle: dict) -> None:
    lesson_ids = [lesson["id"] for lesson in bundle["lessons"]]
    profile["completedLessonIds"].extend(lesson_ids)
    profile["checkpointResults"].append(
        {
            "checkpointId": bundle["checkpoint"]["id"],
            "score": 3,
            "total": 3,
            "completedAt": "2026-07-31",
        }
    )
    profile["reviewCards"].extend(
        {
            "id": f"{bundle['checkpoint']['id']}-word-{index}",
            "hanzi": "学",
            "pinyin": "xué",
            "meaningVi": "học",
            "sourceLessonId": lesson_ids[index // 2],
            "repetitions": 1,
            "intervalDays": 7,
            "dueDate": "2026-08-07",
        }
        for index in range(10)
    )
    topic_number = len(profile.get("topicVocabularyProgress", [])) + 1
    profile.setdefault("topicVocabularyProgress", []).append(
        {
            "topicId": f"daily-topic-{topic_number}",
            "sessionId": f"daily-topic-{topic_number}-session-1",
            "phase": "completed",
            "cardIndex": 10,
            "quizIndex": 10,
            "learnedWordIds": [f"topic-{topic_number}-word-{index}" for index in range(10)],
            "correctWordIds": [f"topic-{topic_number}-word-{index}" for index in range(8)],
            "updatedAt": f"2026-08-{topic_number:02d}T12:00:00Z",
        }
    )


def pass_level_exam(client: TestClient, headers: dict[str, str]) -> None:
    started = client.post("/api/v1/level-exams/attempts", headers=headers)
    assert started.status_code in (200, 201)
    payload = started.json()
    definition = client.app.state.account_repository.get_level_exam(payload["exam_id"])
    for question in definition.questions:
        saved = client.put(
            f"/api/v1/level-exams/attempts/{payload['attempt_id']}",
            json={"question_id": question.id, "option_id": question.correct_option_id,
                  "current_index": 0}, headers=headers,
        )
        assert saved.status_code == 200
    result = client.post(
        f"/api/v1/level-exams/attempts/{payload['attempt_id']}/submit", headers=headers,
    )
    assert result.status_code == 200 and result.json()["passed"] is True


def test_next_path_requires_authentication(tmp_path: Path) -> None:
    client = TestClient(
        create_app(
            database_path=tmp_path / "daily.sqlite3",
            daily_path_generator=FakeDailyPathGenerator(),
        )
    )

    assert client.post("/api/v1/path/next").status_code == 401


def test_next_day_requires_current_day_checkpoint(tmp_path: Path) -> None:
    client = TestClient(
        create_app(
            database_path=tmp_path / "locked-next-day.sqlite3",
            daily_path_generator=FakeDailyPathGenerator(),
        )
    )
    _, headers = register(client)
    profile = ready_profile()
    profile["checkpointResults"] = []
    client.put("/api/v1/profile", json=profile, headers=headers)

    response = client.post("/api/v1/path/next", headers=headers)

    assert response.status_code == 409
    assert "checkpoint của Ngày hiện tại" in response.json()["detail"]


def test_next_day_requires_a_completed_topic_vocabulary_session(
    tmp_path: Path,
) -> None:
    client = TestClient(
        create_app(
            database_path=tmp_path / "locked-topic-session.sqlite3",
            daily_path_generator=FakeDailyPathGenerator(),
        )
    )
    _, headers = register(client)
    profile = ready_profile(score=2, total=3, remembered=6)
    profile["topicVocabularyProgress"] = []
    client.put("/api/v1/profile", json=profile, headers=headers)

    response = client.post("/api/v1/path/next", headers=headers)

    assert response.status_code == 409
    assert "10 từ theo chủ đề" in response.json()["detail"]


def test_creates_and_reuses_a_persisted_next_path(tmp_path: Path) -> None:
    generator = FakeDailyPathGenerator()
    client = TestClient(
        create_app(
            database_path=tmp_path / "daily.sqlite3",
            daily_path_generator=generator,
        )
    )
    _, headers = register(client)
    assert client.put("/api/v1/profile", json=ready_profile(), headers=headers).status_code == 200
    pass_level_exam(client, headers)

    first = client.post("/api/v1/path/next", headers=headers)
    second = client.post("/api/v1/path/next", headers=headers)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert len(generator.calls) == 1
    assert first.json()["level"] == 2
    assert [item["number"] for item in first.json()["lessons"]] == [6, 7, 8, 9, 10]
    assert first.json()["checkpoint"]["title"] == "Checkpoint Bài 6–10"


def test_keeps_the_same_level_when_mastery_is_below_threshold(tmp_path: Path) -> None:
    generator = FakeDailyPathGenerator()
    client = TestClient(
        create_app(
            database_path=tmp_path / "reinforce.sqlite3",
            daily_path_generator=generator,
        )
    )
    _, headers = register(client)
    client.put(
        "/api/v1/profile",
        json=ready_profile(score=2, total=3, remembered=6),
        headers=headers,
    )

    response = client.post("/api/v1/path/next", headers=headers)

    assert response.status_code == 200
    assert response.json()["level"] == 1
    assert generator.calls[0]["checkpoint_rate"] < 0.8
    assert generator.calls[0]["retention_rate"] < 0.7


def test_can_open_day_three_immediately_after_completing_day_two(
    tmp_path: Path,
) -> None:
    generator = FakeDailyPathGenerator()
    client = TestClient(
        create_app(
            database_path=tmp_path / "day-three.sqlite3",
            daily_path_generator=generator,
        )
    )
    _, headers = register(client)
    profile = ready_profile()
    client.put("/api/v1/profile", json=profile, headers=headers)
    pass_level_exam(client, headers)
    day_two = client.post("/api/v1/path/next", headers=headers).json()
    complete_generated_day(profile, day_two)
    client.put("/api/v1/profile", json=profile, headers=headers)
    pass_level_exam(client, headers)

    day_three = client.post("/api/v1/path/next", headers=headers)
    overview = client.get("/api/v1/path", headers=headers)

    assert day_three.status_code == 200
    assert [lesson["number"] for lesson in day_three.json()["lessons"]] == [
        11,
        12,
        13,
        14,
        15,
    ]
    assert overview.json()["current_day_number"] == 3
    assert [day["day_number"] for day in overview.json()["days"]] == [1, 2, 3]


def test_progresses_through_hsk_six_then_completes_the_journey(
    tmp_path: Path,
) -> None:
    client = TestClient(
        create_app(
            database_path=tmp_path / "hsk-six.sqlite3",
            daily_path_generator=FakeDailyPathGenerator(),
        )
    )
    _, headers = register(client)
    profile = ready_profile()
    client.put("/api/v1/profile", json=profile, headers=headers)

    hsk_six_day = None
    for expected_level in range(2, 7):
        pass_level_exam(client, headers)
        response = client.post("/api/v1/path/next", headers=headers)
        assert response.status_code == 200
        bundle = response.json()
        assert bundle["level"] == expected_level
        if expected_level == 6:
            hsk_six_day = bundle
            break
        complete_generated_day(profile, bundle)
        client.put("/api/v1/profile", json=profile, headers=headers)

    assert hsk_six_day is not None
    complete_generated_day(profile, hsk_six_day)
    client.put("/api/v1/profile", json=profile, headers=headers)
    pass_level_exam(client, headers)

    overview = client.get("/api/v1/path", headers=headers)
    after_hsk_six = client.post("/api/v1/path/next", headers=headers)

    assert overview.status_code == 200
    assert overview.json()["current_level"] == 6
    assert overview.json()["completed_all_levels"] is True
    assert overview.json()["days"][-1]["status"] == "completed"
    assert after_hsk_six.status_code == 409
    assert after_hsk_six.json()["detail"] == "Bạn đã hoàn thành lộ trình HSK 1–6."


def test_reads_generated_lessons_checkpoint_and_overview(tmp_path: Path) -> None:
    client = TestClient(
        create_app(
            database_path=tmp_path / "read.sqlite3",
            daily_path_generator=FakeDailyPathGenerator(),
        )
    )
    _, headers = register(client)
    client.put("/api/v1/profile", json=ready_profile(), headers=headers)
    pass_level_exam(client, headers)
    client.post("/api/v1/path/next", headers=headers)

    overview = client.get("/api/v1/path", params={"level": 1}, headers=headers)
    lesson = client.get("/api/v1/path/lessons/6", headers=headers)
    checkpoint = client.get(
        "/api/v1/path/checkpoint",
        params={"start": 6},
        headers=headers,
    )

    assert overview.status_code == 200
    assert len(overview.json()["lessons"]) == 10
    assert overview.json()["current_level"] == 2
    assert overview.json()["current_path_index"] == 2
    assert overview.json()["current_day_number"] == 2
    assert overview.json()["current_difficulty"] == 1
    assert overview.json()["days"] == [
        {
            "day_number": 1,
            "level": 1,
            "difficulty": 1,
            "lesson_start": 1,
            "lesson_end": 5,
            "lesson_ids": [f"hsk1-lesson-{number}" for number in range(1, 6)],
                "checkpoint_id": "hsk1-checkpoint-1-5",
                "completed_lesson_count": 5,
                "topic_vocabulary_completed": True,
                "checkpoint_completed": True,
            "status": "completed",
        },
        {
            "day_number": 2,
            "level": 2,
            "difficulty": 1,
            "lesson_start": 6,
            "lesson_end": 10,
            "lesson_ids": [f"hsk2-lesson-{number}" for number in range(6, 11)],
                "checkpoint_id": "hsk2-checkpoint-6-10",
                "completed_lesson_count": 0,
                "topic_vocabulary_completed": False,
                "checkpoint_completed": False,
            "status": "current",
        },
    ]
    assert lesson.status_code == 200
    assert lesson.json()["number"] == 6
    assert checkpoint.status_code == 200
    assert checkpoint.json()["lesson_ids"] == [
        f"hsk2-lesson-{number}" for number in range(6, 11)
    ]


def test_initial_overview_exposes_day_one_metadata(tmp_path: Path) -> None:
    client = TestClient(
        create_app(
            database_path=tmp_path / "initial-day.sqlite3",
            daily_path_generator=FakeDailyPathGenerator(),
        )
    )
    _, headers = register(client)

    overview = client.get("/api/v1/path", headers=headers)

    assert overview.status_code == 200
    assert overview.json()["current_day_number"] == 1
    assert overview.json()["days"][0]["day_number"] == 1
    assert overview.json()["days"][0]["lesson_start"] == 1
    assert overview.json()["days"][0]["lesson_end"] == 5
    assert overview.json()["days"][0]["completed_lesson_count"] == 0
    assert overview.json()["days"][0]["status"] == "current"


def test_generator_failure_does_not_persist_a_partial_path(tmp_path: Path) -> None:
    generator = FakeDailyPathGenerator(fail=True)
    client = TestClient(
        create_app(
            database_path=tmp_path / "failure.sqlite3",
            daily_path_generator=generator,
        )
    )
    _, headers = register(client)
    client.put("/api/v1/profile", json=ready_profile(), headers=headers)
    pass_level_exam(client, headers)

    failed = client.post("/api/v1/path/next", headers=headers)
    overview = client.get("/api/v1/path", params={"level": 1}, headers=headers)

    assert failed.status_code == 503
    assert failed.json()["detail"] == "AI chưa thể tạo Ngày mới. Vui lòng thử lại."
    assert len(overview.json()["lessons"]) == 5
