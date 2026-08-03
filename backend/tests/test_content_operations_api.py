from copy import deepcopy
from pathlib import Path

from fastapi.testclient import TestClient

from hsk_api.content.learning_path import CHECKPOINT, LESSONS
from hsk_api.main import create_app
from tests.test_daily_paths_api import pass_level_exam


class Generator:
    def __init__(self, *, duplicate: bool = False) -> None:
        self.calls = 0
        self.duplicate = duplicate
        self.last_usage = {"input_tokens": 1200, "output_tokens": 800}

    def generate(self, **context):
        self.calls += 1
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
                title=f"HSK {level} · chủ đề {number}",
                goal=source.goal if self.duplicate else f"Mục tiêu mới {number}",
            )
            if not self.duplicate:
                for word in lesson["vocabulary"]:
                    word["hanzi"] = f"{word['hanzi']}{number}"
            for key in ("dialogue", "vocabulary"):
                for item_index, item in enumerate(lesson[key], 1):
                    item["id"] = f"{lesson['id']}-{key}-{item_index}"
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


def register(client: TestClient, email: str) -> dict[str, str]:
    session = client.post(
        "/api/v1/auth/register",
        json={"display_name": "Tester", "email": email, "password": "matkhau123"},
    ).json()
    return {"Authorization": f"Bearer {session['token']}"}


def ready_profile() -> dict:
    return {
        "version": 1,
        "completedLessonIds": [f"hsk1-lesson-{number}" for number in range(1, 6)],
        "streak": {"current": 1, "longest": 1, "lastActiveDate": "2026-07-31"},
        "reviewCards": [
            {
                "id": f"word-{index}",
                "hanzi": "你",
                "pinyin": "nǐ",
                "meaningVi": "bạn",
                "sourceLessonId": f"hsk1-lesson-{(index // 2) + 1}",
                "repetitions": 1,
                "intervalDays": 7,
                "dueDate": "2026-08-07",
            }
            for index in range(10)
        ],
        "mistakes": [],
        "notebook": [],
        "checkpointResults": [
            {
                "checkpointId": "hsk1-checkpoint-1-5",
                "score": 3,
                "total": 3,
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
        "activityEvents": [],
    }


def test_quality_failure_is_queued_and_not_published(tmp_path: Path) -> None:
    client = TestClient(
        create_app(
            database_path=tmp_path / "quality.sqlite3",
            daily_path_generator=Generator(duplicate=True),
            admin_emails={"admin@example.com"},
        )
    )
    learner = register(client, "learner@example.com")
    admin = register(client, "admin@example.com")
    client.put("/api/v1/profile", json=ready_profile(), headers=learner)
    pass_level_exam(client, learner)

    response = client.post("/api/v1/path/next", headers=learner)
    path = client.get("/api/v1/path", headers=learner)
    drafts = client.get("/api/v1/admin/content?status=pending", headers=admin)

    assert response.status_code == 503
    assert len(path.json()["lessons"]) == 5
    assert drafts.status_code == 200
    assert len(drafts.json()) == 1
    assert "duplicate" in drafts.json()[0]["quality"]["codes"]


def test_quota_is_checked_before_calling_ai_and_usage_is_recorded(tmp_path: Path) -> None:
    generator = Generator()
    client = TestClient(
        create_app(
            database_path=tmp_path / "quota.sqlite3",
            daily_path_generator=generator,
            ai_account_daily_limit=1,
            admin_emails={"admin@example.com"},
        )
    )
    learner = register(client, "learner@example.com")
    admin = register(client, "admin@example.com")
    client.put("/api/v1/profile", json=ready_profile(), headers=learner)
    pass_level_exam(client, learner)

    repository = client.app.state.account_repository
    repository.record_ai_usage(
        account_id=repository.find_by_email("learner@example.com").id,
        operation="daily_path",
        status="success",
        input_tokens=1200,
        output_tokens=800,
    )
    limited = client.post("/api/v1/path/next", headers=learner)
    usage = client.get("/api/v1/admin/usage", headers=admin)

    assert limited.status_code == 429
    assert generator.calls == 0
    assert usage.status_code == 200
    assert usage.json()["today_requests"] == 1
    assert usage.json()["input_tokens"] == 1200
    assert usage.json()["output_tokens"] == 800


def test_only_admin_can_edit_approve_and_reject_content(tmp_path: Path) -> None:
    client = TestClient(
        create_app(
            database_path=tmp_path / "admin.sqlite3",
            daily_path_generator=Generator(duplicate=True),
            admin_emails={"admin@example.com"},
        )
    )
    learner = register(client, "learner@example.com")
    admin = register(client, "admin@example.com")
    client.put("/api/v1/profile", json=ready_profile(), headers=learner)
    pass_level_exam(client, learner)
    client.post("/api/v1/path/next", headers=learner)

    assert client.get("/api/v1/admin/content", headers=learner).status_code == 403
    draft = client.get("/api/v1/admin/content?status=pending", headers=admin).json()[0]
    payload = draft["payload"]
    for index, lesson in enumerate(payload["lessons"], 1):
        lesson["goal"] = f"Mục tiêu đã sửa {index}"
        for word_index, word in enumerate(lesson["vocabulary"], 1):
            word["hanzi"] = f"新{index}{word_index}"

    edited = client.put(
        f"/api/v1/admin/content/{draft['id']}",
        headers=admin,
        json={"payload": payload},
    )
    approved = client.post(
        f"/api/v1/admin/content/{draft['id']}/approve",
        headers=admin,
    )
    path = client.get("/api/v1/path", headers=learner)

    assert edited.status_code == 200
    assert edited.json()["quality"]["passed"] is True
    assert approved.status_code == 200
    assert approved.json()["status"] == "approved"
    assert len(path.json()["lessons"]) == 10
    assert client.post(
        f"/api/v1/admin/content/{draft['id']}/reject",
        headers=admin,
    ).status_code == 409
