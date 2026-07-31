from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from hsk_api.config import get_settings
from hsk_api.routers.health import router as health_router
from hsk_api.routers.lessons import router as lessons_router
from hsk_api.routers.skills import router as skills_router
from hsk_api.routers.learning_path import router as learning_path_router
from hsk_api.routers.auth import router as auth_router
from hsk_api.routers.profile import router as profile_router
from hsk_api.repositories.accounts import AccountRepository
from pathlib import Path
from hsk_api.routers.pronunciation import router as pronunciation_router
from hsk_api.routers.analytics import router as analytics_router
from hsk_api.routers.admin import router as admin_router
from hsk_api.adapters.openai_pronunciation import OpenAIPronunciationAnalyzer
from hsk_api.adapters.openai_speech import OpenAISpeechSynthesizer
from hsk_api.adapters.openai_daily_paths import OpenAIDailyPathGenerator
from hsk_api.services.daily_paths import DailyPathService

_DEFAULT_ANALYZER = object()
_DEFAULT_DAILY_PATH_GENERATOR = object()


def create_app(
    database_path: Path | None = None,
    pronunciation_analyzer=_DEFAULT_ANALYZER,
    speech_synthesizer=_DEFAULT_ANALYZER,
    daily_path_generator=_DEFAULT_DAILY_PATH_GENERATOR,
    admin_emails: set[str] | None = None,
    ai_account_daily_limit: int | None = None,
    ai_system_daily_limit: int | None = None,
) -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title="HSK Learning API",
        version="0.1.0",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "OPTIONS"],
        allow_headers=["*"],
    )
    application.include_router(health_router)
    application.include_router(lessons_router)
    application.include_router(skills_router)
    application.include_router(learning_path_router)
    application.include_router(auth_router)
    application.include_router(profile_router)
    application.include_router(pronunciation_router)
    application.include_router(analytics_router)
    application.include_router(admin_router)
    repository = AccountRepository(database_path or settings.database_path)
    application.state.account_repository = repository
    application.state.admin_emails = {
        email.casefold()
        for email in (
            settings.admin_email_set if admin_emails is None else admin_emails
        )
    }
    application.state.ai_account_daily_limit = (
        settings.ai_account_daily_limit
        if ai_account_daily_limit is None
        else ai_account_daily_limit
    )
    application.state.ai_system_daily_limit = (
        settings.ai_system_daily_limit
        if ai_system_daily_limit is None
        else ai_system_daily_limit
    )
    key = (
        settings.openai_api_key.get_secret_value().strip()
        if settings.openai_api_key else None
    ) or None
    if pronunciation_analyzer is _DEFAULT_ANALYZER:
        pronunciation_analyzer = (
            OpenAIPronunciationAnalyzer(
                key,
                settings.openai_transcription_model,
                settings.openai_timeout_seconds,
                settings.openai_audio_model,
            )
            if key else None
        )
    application.state.pronunciation_analyzer = pronunciation_analyzer
    if speech_synthesizer is _DEFAULT_ANALYZER:
        speech_synthesizer = (
            OpenAISpeechSynthesizer(
                key,
                settings.openai_speech_model,
                settings.openai_speech_voice,
                settings.openai_timeout_seconds,
            )
            if key else None
        )
    application.state.speech_synthesizer = speech_synthesizer
    if daily_path_generator is _DEFAULT_DAILY_PATH_GENERATOR:
        daily_path_generator = (
            OpenAIDailyPathGenerator.from_api_key(
                api_key=key,
                model=settings.openai_model,
                timeout_seconds=settings.openai_daily_path_timeout_seconds,
            )
            if key
            else None
        )
    application.state.daily_path_service = DailyPathService(
        repository=repository,
        generator=daily_path_generator,
        account_daily_limit=application.state.ai_account_daily_limit,
        system_daily_limit=application.state.ai_system_daily_limit,
    )
    return application


app = create_app()
