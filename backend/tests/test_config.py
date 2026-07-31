from hsk_api.config import Settings


def test_api_key_is_server_only_and_hidden_from_repr() -> None:
    settings = Settings(openai_api_key="test-secret-value")

    assert settings.openai_api_key.get_secret_value() == "test-secret-value"
    assert "test-secret-value" not in repr(settings)
    assert "test-secret-value" not in settings.model_dump_json()
