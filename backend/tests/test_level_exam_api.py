from pathlib import Path

from fastapi.testclient import TestClient

from hsk_api.main import create_app
from tests.test_daily_paths_api import ready_profile


def learner(tmp_path: Path) -> tuple[TestClient, dict[str, str]]:
    client = TestClient(create_app(database_path=tmp_path / "level-exam.sqlite3"))
    response = client.post("/api/v1/auth/register", json={
        "display_name": "Người học", "email": "exam@example.com", "password": "matkhau123",
    })
    return client, {"Authorization": f"Bearer {response.json()['token']}"}


def make_eligible(client: TestClient, headers: dict[str, str]) -> None:
    assert client.put("/api/v1/profile", json=ready_profile(), headers=headers).status_code == 200


def test_level_exam_requires_authentication_and_mastery(tmp_path: Path) -> None:
    client, headers = learner(tmp_path)
    assert client.get("/api/v1/level-exams/status").status_code == 401
    status = client.get("/api/v1/level-exams/status", headers=headers)
    assert status.status_code == 200
    assert status.json()["eligible"] is False
    assert client.post("/api/v1/level-exams/attempts", headers=headers).status_code == 409


def test_starts_fixed_twenty_question_exam_without_leaking_answers(tmp_path: Path) -> None:
    client, headers = learner(tmp_path)
    make_eligible(client, headers)
    response = client.post("/api/v1/level-exams/attempts", headers=headers)
    assert response.status_code == 201
    payload = response.json()
    assert len(payload["questions"]) == 20
    assert {skill: sum(q["skill"] == skill for q in payload["questions"])
            for skill in ("vocabulary", "grammar", "reading", "listening")} == {
                "vocabulary": 5, "grammar": 5, "reading": 5, "listening": 5,
            }
    assert all("correct_option_id" not in question and "audio_text" not in question
               for question in payload["questions"])


def test_saves_and_resumes_exam_then_scores_all_correct(tmp_path: Path) -> None:
    client, headers = learner(tmp_path)
    make_eligible(client, headers)
    started = client.post("/api/v1/level-exams/attempts", headers=headers).json()
    attempt_id = started["attempt_id"]
    repository = client.app.state.account_repository
    definition = repository.get_level_exam(started["exam_id"])
    answers = {question.id: question.correct_option_id for question in definition.questions}
    first_id, first_option = next(iter(answers.items()))
    saved = client.put(
        f"/api/v1/level-exams/attempts/{attempt_id}",
        json={"question_id": first_id, "option_id": first_option, "flagged": True, "current_index": 1},
        headers=headers,
    )
    assert saved.status_code == 200
    resumed = client.post("/api/v1/level-exams/attempts", headers=headers)
    assert resumed.status_code == 200
    assert resumed.json()["selections"][first_id] == first_option
    assert first_id in resumed.json()["flagged_question_ids"]
    for question_id, option_id in answers.items():
        client.put(f"/api/v1/level-exams/attempts/{attempt_id}", json={
            "question_id": question_id, "option_id": option_id, "current_index": 0,
        }, headers=headers)
    result = client.post(f"/api/v1/level-exams/attempts/{attempt_id}/submit", headers=headers)
    assert result.status_code == 200
    assert result.json()["passed"] is True
    assert result.json()["overall_percent"] == 100
    assert all(item["percent"] == 100 for item in result.json()["skills"])


def test_each_skill_must_reach_sixty_percent_and_retake_changes_order(tmp_path: Path) -> None:
    client, headers = learner(tmp_path)
    make_eligible(client, headers)
    started = client.post("/api/v1/level-exams/attempts", headers=headers).json()
    definition = client.app.state.account_repository.get_level_exam(started["exam_id"])
    for index, question in enumerate(definition.questions):
        option = question.correct_option_id
        if question.skill == "reading" and index < 18:
            option = next(item.id for item in question.options if item.id != option)
        client.put(f"/api/v1/level-exams/attempts/{started['attempt_id']}", json={
            "question_id": question.id, "option_id": option, "current_index": 0,
        }, headers=headers)
    result = client.post(
        f"/api/v1/level-exams/attempts/{started['attempt_id']}/submit", headers=headers,
    ).json()
    assert result["overall_percent"] >= 80
    assert result["passed"] is False
    retake = client.post("/api/v1/level-exams/attempts", headers=headers)
    assert retake.status_code == 201
    assert [q["id"] for q in retake.json()["questions"]] != [q["id"] for q in started["questions"]]
