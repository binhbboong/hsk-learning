from hsk_api.config import Settings


def test_api_key_is_server_only_and_hidden_from_repr() -> None:
    settings = Settings(openai_api_key="test-secret-value")

    assert settings.openai_api_key.get_secret_value() == "test-secret-value"
    assert "test-secret-value" not in repr(settings)
    assert "test-secret-value" not in settings.model_dump_json()


def test_all_text_generation_defaults_use_gpt_4_1_mini() -> None:
    settings = Settings(_env_file=None)

    assert settings.openai_model == "gpt-4.1-mini"
    assert settings.openai_topic_vocabulary_model == "gpt-4.1-mini"
    assert settings.openai_transcription_model != "gpt-4.1-mini"
    assert settings.openai_audio_model != "gpt-4.1-mini"
    assert settings.openai_speech_model != "gpt-4.1-mini"
