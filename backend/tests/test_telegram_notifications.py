from datetime import UTC, datetime
from pathlib import Path

from fastapi.testclient import TestClient

from hsk_api.main import create_app


class FakeTelegramSender:
    def __init__(self) -> None:
        self.messages: list[tuple[str, str]] = []

    def send_message(self, chat_id: str, text: str) -> None:
        self.messages.append((chat_id, text))


def register(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "display_name": "Bình",
            "email": "binh@example.com",
            "password": "matkhau123",
        },
    )
    return {"Authorization": f"Bearer {response.json()['token']}"}


def completed_profile() -> dict:
    return {
        "completedLessonIds": [f"hsk1-lesson-{number}" for number in range(1, 6)],
        "checkpointResults": [{"checkpointId": "hsk1-checkpoint-1-5"}],
        "topicVocabularyProgress": [{"phase": "completed"}],
    }


def configured_app(tmp_path: Path, sender: FakeTelegramSender, hour_utc: int):
    return create_app(
        database_path=tmp_path / f"telegram-{hour_utc}.sqlite3",
        telegram_sender=sender,
        telegram_chat_id="123456",
        telegram_account_email="binh@example.com",
        cron_secret="cron-test-secret",
        reminder_clock=lambda: datetime(2026, 8, 3, hour_utc, tzinfo=UTC),
    )


def test_cron_rejects_requests_without_the_secret(tmp_path: Path) -> None:
    sender = FakeTelegramSender()
    client = TestClient(configured_app(tmp_path, sender, hour_utc=11))
    register(client)

    response = client.get("/api/cron/learning-reminder")

    assert response.status_code == 401
    assert sender.messages == []


def test_does_not_remind_before_18h_vietnam_time(tmp_path: Path) -> None:
    sender = FakeTelegramSender()
    client = TestClient(configured_app(tmp_path, sender, hour_utc=10))
    register(client)

    response = client.get(
        "/api/cron/learning-reminder",
        headers={"Authorization": "Bearer cron-test-secret"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "outside_reminder_window"
    assert sender.messages == []


def test_reminds_each_cron_run_from_18h_while_day_is_incomplete(tmp_path: Path) -> None:
    sender = FakeTelegramSender()
    client = TestClient(configured_app(tmp_path, sender, hour_utc=11))
    register(client)
    headers = {"Authorization": "Bearer cron-test-secret"}

    first = client.get("/api/cron/learning-reminder", headers=headers)
    second = client.get("/api/cron/learning-reminder", headers=headers)

    assert first.json()["status"] == "reminder_sent"
    assert second.json()["status"] == "reminder_sent"
    assert len(sender.messages) == 2
    assert "Ngày 1" in sender.messages[0][1]
    assert "chưa hoàn thành" in sender.messages[0][1]


def test_completed_day_is_not_reminded(tmp_path: Path) -> None:
    sender = FakeTelegramSender()
    client = TestClient(configured_app(tmp_path, sender, hour_utc=11))
    profile_headers = register(client)
    client.put("/api/v1/profile", json=completed_profile(), headers=profile_headers)
    sender.messages.clear()

    response = client.get(
        "/api/cron/learning-reminder",
        headers={"Authorization": "Bearer cron-test-secret"},
    )

    assert response.json()["status"] == "already_completed"
    assert sender.messages == []


def test_profile_transition_sends_one_completion_message(tmp_path: Path) -> None:
    sender = FakeTelegramSender()
    client = TestClient(configured_app(tmp_path, sender, hour_utc=9))
    headers = register(client)

    first = client.put("/api/v1/profile", json=completed_profile(), headers=headers)
    second = client.put("/api/v1/profile", json=completed_profile(), headers=headers)

    assert first.status_code == 200
    assert second.status_code == 200
    assert len(sender.messages) == 1
    assert "đã hoàn thành lộ trình Ngày 1" in sender.messages[0][1]
