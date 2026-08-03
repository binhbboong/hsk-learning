from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: SecretStr | None = None
    openai_model: str = "gpt-5.6"
    openai_transcription_model: str = "gpt-4o-transcribe"
    openai_audio_model: str = "gpt-audio"
    openai_speech_model: str = "gpt-4o-mini-tts"
    openai_speech_voice: str = "coral"
    openai_timeout_seconds: float = 15.0
    openai_topic_vocabulary_model: str = "gpt-4.1-mini"
    openai_topic_vocabulary_timeout_seconds: float = 60.0
    openai_daily_path_timeout_seconds: float = 180.0
    ai_account_daily_limit: int = 10
    ai_system_daily_limit: int = 50
    admin_emails: str = ""
    allowed_origins: str = "http://localhost:4200"
    database_url: SecretStr | None = None
    database_path: Path = Path("data/hsk_learning.sqlite3")

    @property
    def origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]

    @property
    def admin_email_set(self) -> set[str]:
        return {
            email.strip().casefold()
            for email in self.admin_emails.split(",")
            if email.strip()
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
