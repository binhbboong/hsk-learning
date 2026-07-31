from pathlib import Path

from fastapi.testclient import TestClient

from hsk_api.main import create_app


def register(client: TestClient, email: str) -> dict[str, str]:
    session = client.post(
        "/api/v1/auth/register",
        json={"display_name": "Mai", "email": email, "password": "matkhau123"},
    ).json()
    return {"Authorization": f"Bearer {session['token']}"}


def test_returns_seven_day_activity_retention_weakness_and_recommendation(
    tmp_path: Path,
) -> None:
    client = TestClient(create_app(database_path=tmp_path / "analytics.sqlite3"))
    headers = register(client, "insights@example.com")
    profile = {
        "version": 1,
        "completedLessonIds": ["hsk1-lesson-1"],
        "streak": {"current": 2, "longest": 2, "lastActiveDate": "2026-07-31"},
        "reviewCards": [
            {
                "id": "word-1", "hanzi": "你", "pinyin": "nǐ", "meaningVi": "bạn",
                "sourceLessonId": "hsk1-lesson-1", "repetitions": 0,
                "intervalDays": 1, "dueDate": "2026-07-31",
                "lastReviewedAt": "2026-07-30T08:00:00Z",
            },
            {
                "id": "word-2", "hanzi": "好", "pinyin": "hǎo", "meaningVi": "tốt",
                "sourceLessonId": "hsk1-lesson-1", "repetitions": 2,
                "intervalDays": 7, "dueDate": "2026-08-07",
                "lastReviewedAt": "2026-07-29T08:00:00Z",
            },
        ],
        "mistakes": [
            {
                "id": "m1", "sourceLessonId": "hsk1-lesson-1",
                "kind": "listening", "prompt": "Nghe câu", "correctAnswer": "A",
                "explanationVi": "Nghe lại",
            },
            {
                "id": "m2", "sourceLessonId": "hsk1-lesson-1",
                "kind": "listening", "prompt": "Nghe câu khác", "correctAnswer": "B",
                "explanationVi": "Nghe lại",
            },
        ],
        "notebook": [], "checkpointResults": [],
        "activityEvents": [
            {"kind": "lesson", "occurredAt": "2026-07-30T08:00:00Z"},
            {"kind": "review", "occurredAt": "2026-07-31T08:00:00Z"},
            {
                "kind": "pronunciation",
                "occurredAt": "2026-07-31T08:10:00Z",
                "score": 72,
            },
        ],
    }
    client.put("/api/v1/profile", json=profile, headers=headers)

    response = client.get(
        "/api/v1/analytics/learning?as_of=2026-07-31",
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body["activity_days"]) == 7
    assert body["activity_days"][-1]["active"] is True
    assert body["activity_days"][-2]["active"] is True
    assert body["retention_30d"]["rate"] == 0.5
    assert body["retention_30d"]["sample_size"] == 2
    assert body["weaknesses"][0]["skill"] == "listening"
    assert body["recommendation"]["route"] == "/learn/review"
    assert body["recommendation"]["query_params"] == {"source": "mistakes"}


def test_new_learner_has_beginner_safe_empty_insights(tmp_path: Path) -> None:
    client = TestClient(create_app(database_path=tmp_path / "empty.sqlite3"))
    headers = register(client, "new@example.com")

    response = client.get(
        "/api/v1/analytics/learning?as_of=2026-07-31",
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["retention_30d"]["rate"] is None
    assert body["recommendation"]["title"] == "Bắt đầu Bài 1"
    assert body["recommendation"]["route"] == "/learn/lesson/1"

