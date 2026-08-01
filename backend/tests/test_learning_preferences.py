from pathlib import Path

from fastapi.testclient import TestClient

from hsk_api.main import create_app
from tests.test_daily_paths_api import FakeDailyPathGenerator, pass_level_exam, ready_profile, register


def test_preferences_are_validated_persisted_and_sent_to_daily_generator(tmp_path: Path) -> None:
    generator = FakeDailyPathGenerator()
    client = TestClient(create_app(
        database_path=tmp_path / "preferences.sqlite3", daily_path_generator=generator,
    ))
    _, headers = register(client)
    profile = ready_profile()
    profile["learningPreferences"] = {
        "goal": "travel", "dailyMinutes": 20,
        "preferredTopics": ["food", "transport", "shopping"],
    }
    assert client.put("/api/v1/profile", json=profile, headers=headers).status_code == 200
    assert client.get("/api/v1/profile", headers=headers).json()["learningPreferences"] == profile["learningPreferences"]
    invalid = {**profile, "learningPreferences": {**profile["learningPreferences"],
               "preferredTopics": ["food", "transport", "shopping", "family"]}}
    assert client.put("/api/v1/profile", json=invalid, headers=headers).status_code == 422
    pass_level_exam(client, headers)
    assert client.post("/api/v1/path/next", headers=headers).status_code == 200
    assert generator.calls[-1]["learning_goal"] == "travel"
    assert generator.calls[-1]["daily_minutes"] == 20
    assert generator.calls[-1]["preferred_topics"] == ["food", "transport", "shopping"]
