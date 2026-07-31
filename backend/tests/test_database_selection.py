from pathlib import Path

import hsk_api.main as main_module


def test_create_app_prefers_explicit_postgres_database_url(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class FakeRepository:
        def __init__(
            self,
            database_path: Path | None = None,
            database_url: str | None = None,
        ) -> None:
            captured["database_path"] = database_path
            captured["database_url"] = database_url

    monkeypatch.setattr(main_module, "AccountRepository", FakeRepository)

    main_module.create_app(
        database_path=Path("ignored.sqlite3"),
        database_url="postgresql://learner:secret@db.example/hsk",
        pronunciation_analyzer=None,
        speech_synthesizer=None,
        daily_path_generator=None,
    )

    assert captured == {
        "database_path": None,
        "database_url": "postgresql://learner:secret@db.example/hsk",
    }


def test_create_app_keeps_sqlite_for_local_tests(monkeypatch, tmp_path: Path) -> None:
    captured: dict[str, object] = {}

    class FakeRepository:
        def __init__(
            self,
            database_path: Path | None = None,
            database_url: str | None = None,
        ) -> None:
            captured["database_path"] = database_path
            captured["database_url"] = database_url

    monkeypatch.setattr(main_module, "AccountRepository", FakeRepository)
    path = tmp_path / "local.sqlite3"

    main_module.create_app(
        database_path=path,
        pronunciation_analyzer=None,
        speech_synthesizer=None,
        daily_path_generator=None,
    )

    assert captured == {"database_path": path, "database_url": None}
