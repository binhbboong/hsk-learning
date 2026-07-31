from pathlib import Path

from fastapi.testclient import TestClient

from hsk_api.main import create_app


def make_client(tmp_path: Path) -> TestClient:
    return TestClient(create_app(database_path=tmp_path / "accounts.sqlite3"))


def test_register_returns_user_and_session_without_password(tmp_path: Path) -> None:
    client = make_client(tmp_path)

    response = client.post(
        "/api/v1/auth/register",
        json={"display_name": "Mai", "email": "mai@example.com", "password": "hocTiengTrung1"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["user"]["display_name"] == "Mai"
    assert payload["user"]["email"] == "mai@example.com"
    assert payload["token"]
    assert "password" not in str(payload).lower()
    assert client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {payload['token']}"},
    ).status_code == 200


def test_registration_validates_and_rejects_duplicate_email(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    account = {"display_name": "Mai", "email": "MAI@example.com", "password": "hocTiengTrung1"}
    assert client.post("/api/v1/auth/register", json=account).status_code == 201

    duplicate = client.post("/api/v1/auth/register", json={**account, "email": "mai@example.com"})
    weak = client.post("/api/v1/auth/register", json={**account, "email": "new@example.com", "password": "short"})

    assert duplicate.status_code == 409
    assert weak.status_code == 422


def test_login_logout_and_invalid_credentials(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    client.post(
        "/api/v1/auth/register",
        json={"display_name": "An", "email": "an@example.com", "password": "matkhau123"},
    )

    invalid = client.post(
        "/api/v1/auth/login",
        json={"email": "an@example.com", "password": "khong-dung"},
    )
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "AN@example.com", "password": "matkhau123"},
    )
    token = login.json()["token"]
    logout = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert invalid.status_code == 401
    assert invalid.json()["detail"] == "Email hoặc mật khẩu không đúng."
    assert login.status_code == 200
    assert logout.status_code == 204
    assert client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    ).status_code == 401
