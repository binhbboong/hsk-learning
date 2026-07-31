from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_health_endpoint_reports_ready_without_secrets() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_recommended_lesson_returns_complete_hsk1_fallback() -> None:
    response = client.get("/api/v1/lessons/recommended", params={"level": 1, "size": 5})

    assert response.status_code == 200
    lesson = response.json()
    assert lesson["level"] == 1
    assert lesson["source"] == "fallback"
    assert len(lesson["cards"]) == 5

    required_fields = {
        "id",
        "hanzi",
        "pinyin",
        "sino_vietnamese",
        "meaning_vi",
        "example_zh",
        "example_vi",
    }
    assert all(required_fields <= card.keys() for card in lesson["cards"])


def test_recommended_lesson_rejects_non_mvp_shape() -> None:
    response = client.get("/api/v1/lessons/recommended", params={"level": 2, "size": 10})

    assert response.status_code == 422


def test_configured_frontend_origin_is_allowed_by_cors() -> None:
    response = client.options(
        "/api/v1/lessons/recommended",
        headers={
            "Origin": "http://localhost:4200",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:4200"
