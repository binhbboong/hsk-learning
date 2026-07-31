from pathlib import Path

from fastapi.testclient import TestClient

from hsk_api.main import create_app


def register(client: TestClient, email: str) -> str:
    response = client.post(
        "/api/v1/auth/register",
        json={"display_name": f"Bạn {email.split('@')[0].upper()}", "email": email, "password": "matkhau123"},
    )
    return response.json()["token"]


def test_each_account_has_an_isolated_learning_profile(tmp_path: Path) -> None:
    client = TestClient(create_app(database_path=tmp_path / "profiles.sqlite3"))
    token_a = register(client, "a@example.com")
    token_b = register(client, "b@example.com")
    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}
    profile_a = {
        "version": 1,
        "completedLessonIds": ["hsk1-lesson-1"],
        "streak": {"current": 1, "longest": 1, "lastActiveDate": "2026-07-31"},
        "reviewCards": [],
        "mistakes": [],
        "notebook": [],
        "checkpointResults": [],
    }

    assert client.put("/api/v1/profile", json=profile_a, headers=headers_a).status_code == 200
    assert client.get("/api/v1/profile", headers=headers_a).json()["completedLessonIds"] == ["hsk1-lesson-1"]
    assert client.get("/api/v1/profile", headers=headers_b).json()["completedLessonIds"] == []


def test_profile_requires_a_valid_session(tmp_path: Path) -> None:
    client = TestClient(create_app(database_path=tmp_path / "protected.sqlite3"))

    assert client.get("/api/v1/profile").status_code == 401
    assert client.put("/api/v1/profile", json={}).status_code == 401
