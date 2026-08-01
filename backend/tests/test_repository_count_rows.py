from hsk_api.repositories.accounts import AccountRepository


class DictCountCursor:
    def __init__(self, total: int) -> None:
        self.total = total

    def fetchone(self) -> dict[str, int]:
        return {"total": self.total}


class DictCountConnection:
    def __init__(self, total: int) -> None:
        self.total = total

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> None:
        return None

    def execute(self, _query: str, _values=()) -> DictCountCursor:
        return DictCountCursor(self.total)


def repository_with_dict_count(monkeypatch, total: int) -> AccountRepository:
    repository = AccountRepository.__new__(AccountRepository)
    monkeypatch.setattr(repository, "_connect", lambda: DictCountConnection(total))
    return repository


def test_ai_usage_count_supports_postgres_dict_rows(monkeypatch) -> None:
    repository = repository_with_dict_count(monkeypatch, 3)

    assert repository.ai_request_count_today("learner-1") == 3


def test_completed_exam_count_supports_postgres_dict_rows(monkeypatch) -> None:
    repository = repository_with_dict_count(monkeypatch, 4)

    assert repository.count_completed_level_exam_attempts("learner-1", 2) == 4
