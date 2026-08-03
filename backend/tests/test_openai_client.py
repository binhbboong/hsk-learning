from hsk_api.adapters.openai_client import create_openai_client


def test_client_uses_the_official_api_when_an_ambient_base_url_exists(
    monkeypatch,
) -> None:
    monkeypatch.setenv("OPENAI_BASE_URL", "https://proxy.invalid/v1")

    client = create_openai_client("test-key", 15)
    try:
        assert str(client.base_url) == "https://api.openai.com/v1/"
    finally:
        client.close()
