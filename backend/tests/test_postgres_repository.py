import os
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from hsk_api.main import create_app


POSTGRES_URL = os.getenv("TEST_POSTGRES_URL")


@pytest.mark.skipif(not POSTGRES_URL, reason="TEST_POSTGRES_URL is not configured")
def test_postgres_persists_account_and_profile_across_app_instances() -> None:
    email = f"postgres-{uuid4().hex}@example.com"
    account = {
        "display_name": "Postgres learner",
        "email": email,
        "password": "matkhau123",
    }
    first = TestClient(
        create_app(
            database_url=POSTGRES_URL,
            pronunciation_analyzer=None,
            speech_synthesizer=None,
            daily_path_generator=None,
        )
    )
    registered = first.post("/api/v1/auth/register", json=account)
    assert registered.status_code == 201
    headers = {"Authorization": f"Bearer {registered.json()['token']}"}
    profile = first.get("/api/v1/profile", headers=headers).json()
    profile["completedLessonIds"] = ["hsk1-lesson-1"]
    assert first.put("/api/v1/profile", headers=headers, json=profile).status_code == 200

    second = TestClient(
        create_app(
            database_url=POSTGRES_URL,
            pronunciation_analyzer=None,
            speech_synthesizer=None,
            daily_path_generator=None,
        )
    )
    login = second.post(
        "/api/v1/auth/login",
        json={"email": email, "password": account["password"]},
    )

    assert login.status_code == 200
    persisted = second.get(
        "/api/v1/profile",
        headers={"Authorization": f"Bearer {login.json()['token']}"},
    )
    assert persisted.status_code == 200
    assert persisted.json()["completedLessonIds"] == ["hsk1-lesson-1"]
