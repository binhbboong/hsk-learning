import json
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from uuid import uuid4

import psycopg
from psycopg.rows import dict_row

from hsk_api.auth.security import hash_token
from hsk_api.models.account import AccountRecord, LearningProfilePayload
from hsk_api.models.content_ops import ContentDraft, QualityReport, UsageSummary
from hsk_api.models.learning_loop import DailyPathBundle


EMPTY_PROFILE = LearningProfilePayload(
    streak={"current": 0, "longest": 0, "lastActiveDate": None},
)


class DatabaseConnection:
    def __init__(self, raw_connection: Any, dialect: str) -> None:
        self.raw_connection = raw_connection
        self.dialect = dialect

    def execute(self, query: str, values: tuple | list = ()):
        if self.dialect == "postgresql":
            query = query.replace("?", "%s")
        return self.raw_connection.execute(query, values)

    def executescript(self, script: str) -> None:
        if self.dialect == "sqlite":
            self.raw_connection.executescript(script)
            return
        for statement in script.split(";"):
            if statement.strip():
                self.execute(statement)

    def __enter__(self) -> "DatabaseConnection":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        try:
            if exc_type is None:
                self.raw_connection.commit()
            else:
                self.raw_connection.rollback()
        finally:
            self.raw_connection.close()


class AccountRepository:
    def __init__(
        self,
        database_path: Path | None = None,
        database_url: str | None = None,
    ) -> None:
        if database_url:
            if not database_url.startswith(("postgresql://", "postgres://")):
                raise ValueError("DATABASE_URL must use the PostgreSQL protocol")
            self.database_url = database_url
            self.database_path = None
            self.dialect = "postgresql"
        elif database_path is not None:
            self.database_url = None
            self.database_path = database_path
            self.database_path.parent.mkdir(parents=True, exist_ok=True)
            self.dialect = "sqlite"
        else:
            raise ValueError("A database_path or database_url is required")
        self._initialize()

    def _connect(self) -> DatabaseConnection:
        if self.dialect == "postgresql":
            connection = psycopg.connect(self.database_url, row_factory=dict_row)
            return DatabaseConnection(connection, self.dialect)
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return DatabaseConnection(connection, self.dialect)

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS accounts (
                    id TEXT PRIMARY KEY,
                    display_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS sessions (
                    token_hash TEXT PRIMARY KEY,
                    account_id TEXT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
                    expires_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS learning_profiles (
                    account_id TEXT PRIMARY KEY REFERENCES accounts(id) ON DELETE CASCADE,
                    payload TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS daily_paths (
                    account_id TEXT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
                    path_index INTEGER NOT NULL,
                    level INTEGER NOT NULL,
                    payload TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY(account_id, path_index)
                );
                CREATE TABLE IF NOT EXISTS content_drafts (
                    id TEXT PRIMARY KEY,
                    account_id TEXT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
                    path_index INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    quality TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    reviewed_by TEXT,
                    UNIQUE(account_id, path_index)
                );
                CREATE TABLE IF NOT EXISTS ai_usage (
                    id TEXT PRIMARY KEY,
                    account_id TEXT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
                    operation TEXT NOT NULL,
                    status TEXT NOT NULL,
                    input_tokens INTEGER NOT NULL DEFAULT 0,
                    output_tokens INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL
                );
                """
            )

    def create_account(self, display_name: str, email: str, password_hash: str) -> AccountRecord | None:
        account = AccountRecord(
            id=str(uuid4()),
            display_name=display_name.strip(),
            email=email.strip().lower(),
            password_hash=password_hash,
            created_at=datetime.now(UTC),
        )
        try:
            with self._connect() as connection:
                connection.execute(
                    "INSERT INTO accounts VALUES (?, ?, ?, ?, ?)",
                    (
                        account.id,
                        account.display_name,
                        account.email,
                        account.password_hash,
                        account.created_at.isoformat(),
                    ),
                )
                connection.execute(
                    "INSERT INTO learning_profiles VALUES (?, ?, ?)",
                    (
                        account.id,
                        EMPTY_PROFILE.model_dump_json(),
                        account.created_at.isoformat(),
                    ),
                )
        except (sqlite3.IntegrityError, psycopg.IntegrityError):
            return None
        return account

    def find_by_email(self, email: str) -> AccountRecord | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM accounts WHERE email = ?",
                (email.strip().lower(),),
            ).fetchone()
        return self._to_account(row)

    def create_session(self, account_id: str, token: str) -> None:
        expires_at = datetime.now(UTC) + timedelta(days=30)
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO sessions VALUES (?, ?, ?)",
                (hash_token(token), account_id, expires_at.isoformat()),
            )

    def account_for_token(self, token: str) -> AccountRecord | None:
        now = datetime.now(UTC).isoformat()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT accounts.* FROM accounts
                JOIN sessions ON sessions.account_id = accounts.id
                WHERE sessions.token_hash = ? AND sessions.expires_at > ?
                """,
                (hash_token(token), now),
            ).fetchone()
        return self._to_account(row)

    def revoke_session(self, token: str) -> None:
        with self._connect() as connection:
            connection.execute(
                "DELETE FROM sessions WHERE token_hash = ?",
                (hash_token(token),),
            )

    def get_profile(self, account_id: str) -> LearningProfilePayload:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT payload FROM learning_profiles WHERE account_id = ?",
                (account_id,),
            ).fetchone()
        if row is None:
            return EMPTY_PROFILE.model_copy(deep=True)
        return LearningProfilePayload.model_validate(json.loads(row["payload"]))

    def save_profile(
        self,
        account_id: str,
        profile: LearningProfilePayload,
    ) -> LearningProfilePayload:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO learning_profiles(account_id, payload, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(account_id) DO UPDATE SET payload = excluded.payload,
                updated_at = excluded.updated_at
                """,
                (account_id, profile.model_dump_json(), datetime.now(UTC).isoformat()),
            )
        return profile

    def list_daily_paths(self, account_id: str) -> list[DailyPathBundle]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT payload FROM daily_paths
                WHERE account_id = ?
                ORDER BY path_index
                """,
                (account_id,),
            ).fetchall()
        return [
            DailyPathBundle.model_validate(json.loads(row["payload"]))
            for row in rows
        ]

    def get_daily_path(
        self,
        account_id: str,
        path_index: int,
    ) -> DailyPathBundle | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT payload FROM daily_paths
                WHERE account_id = ? AND path_index = ?
                """,
                (account_id, path_index),
            ).fetchone()
        if row is None:
            return None
        return DailyPathBundle.model_validate(json.loads(row["payload"]))

    def save_daily_path(
        self,
        account_id: str,
        bundle: DailyPathBundle,
    ) -> DailyPathBundle:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO daily_paths(
                    account_id, path_index, level, payload, created_at
                )
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(account_id, path_index) DO NOTHING
                """,
                (
                    account_id,
                    bundle.path_index,
                    bundle.level,
                    bundle.model_dump_json(),
                    datetime.now(UTC).isoformat(),
                ),
            )
        stored = self.get_daily_path(account_id, bundle.path_index)
        if stored is None:
            raise RuntimeError("Daily path could not be persisted")
        return stored

    def save_content_draft(
        self,
        *,
        account_id: str,
        path_index: int,
        payload: dict,
        quality: QualityReport,
        status: str,
    ) -> ContentDraft:
        now = datetime.now(UTC).isoformat()
        draft_id = str(uuid4())
        with self._connect() as connection:
            existing = connection.execute(
                "SELECT id, created_at FROM content_drafts WHERE account_id = ? AND path_index = ?",
                (account_id, path_index),
            ).fetchone()
            if existing:
                draft_id = existing["id"]
                created_at = existing["created_at"]
            else:
                created_at = now
            connection.execute(
                """
                INSERT INTO content_drafts(
                    id, account_id, path_index, status, payload, quality,
                    created_at, updated_at, reviewed_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL)
                ON CONFLICT(account_id, path_index) DO UPDATE SET
                    status=excluded.status, payload=excluded.payload,
                    quality=excluded.quality, updated_at=excluded.updated_at,
                    reviewed_by=NULL
                """,
                (
                    draft_id,
                    account_id,
                    path_index,
                    status,
                    json.dumps(payload, ensure_ascii=False),
                    quality.model_dump_json(),
                    created_at,
                    now,
                ),
            )
        draft = self.get_content_draft(draft_id)
        if draft is None:
            raise RuntimeError("Content draft could not be persisted")
        return draft

    def list_content_drafts(self, status: str | None = None) -> list[ContentDraft]:
        query = "SELECT * FROM content_drafts"
        values: tuple = ()
        if status:
            query += " WHERE status = ?"
            values = (status,)
        query += " ORDER BY updated_at DESC"
        with self._connect() as connection:
            rows = connection.execute(query, values).fetchall()
        return [self._to_content_draft(row) for row in rows]

    def get_content_draft(self, draft_id: str) -> ContentDraft | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM content_drafts WHERE id = ?",
                (draft_id,),
            ).fetchone()
        return self._to_content_draft(row) if row else None

    def update_content_draft(
        self,
        draft_id: str,
        *,
        payload: dict,
        quality: QualityReport,
    ) -> ContentDraft | None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE content_drafts
                SET payload = ?, quality = ?, updated_at = ?
                WHERE id = ? AND status = 'pending'
                """,
                (
                    json.dumps(payload, ensure_ascii=False),
                    quality.model_dump_json(),
                    datetime.now(UTC).isoformat(),
                    draft_id,
                ),
            )
        return self.get_content_draft(draft_id)

    def decide_content_draft(
        self,
        draft_id: str,
        *,
        status: str,
        reviewed_by: str,
    ) -> ContentDraft | None:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE content_drafts
                SET status = ?, reviewed_by = ?, updated_at = ?
                WHERE id = ? AND status = 'pending'
                """,
                (status, reviewed_by, datetime.now(UTC).isoformat(), draft_id),
            )
        if cursor.rowcount == 0:
            return None
        return self.get_content_draft(draft_id)

    def record_ai_usage(
        self,
        *,
        account_id: str,
        operation: str,
        status: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO ai_usage VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    str(uuid4()),
                    account_id,
                    operation,
                    status,
                    max(0, input_tokens),
                    max(0, output_tokens),
                    datetime.now(UTC).isoformat(),
                ),
            )

    def ai_request_count_today(self, account_id: str | None = None) -> int:
        today = datetime.now(UTC).date().isoformat()
        query = "SELECT COUNT(*) FROM ai_usage WHERE substr(created_at, 1, 10) = ?"
        values: list[str] = [today]
        if account_id:
            query += " AND account_id = ?"
            values.append(account_id)
        with self._connect() as connection:
            return int(connection.execute(query, tuple(values)).fetchone()[0])

    def usage_summary(
        self,
        *,
        account_daily_limit: int,
        system_daily_limit: int,
    ) -> UsageSummary:
        today = datetime.now(UTC).date().isoformat()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT COUNT(*) total,
                       SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) successes,
                       SUM(CASE WHEN status != 'success' THEN 1 ELSE 0 END) failures,
                       COALESCE(SUM(input_tokens), 0) input_tokens,
                       COALESCE(SUM(output_tokens), 0) output_tokens
                FROM ai_usage WHERE substr(created_at, 1, 10) = ?
                """,
                (today,),
            ).fetchone()
        return UsageSummary(
            date=today,
            today_requests=row["total"],
            successful_requests=row["successes"] or 0,
            failed_requests=row["failures"] or 0,
            input_tokens=row["input_tokens"],
            output_tokens=row["output_tokens"],
            account_daily_limit=account_daily_limit,
            system_daily_limit=system_daily_limit,
        )

    @staticmethod
    def _to_content_draft(row: Any) -> ContentDraft:
        return ContentDraft(
            id=row["id"],
            account_id=row["account_id"],
            path_index=row["path_index"],
            status=row["status"],
            payload=json.loads(row["payload"]),
            quality=QualityReport.model_validate_json(row["quality"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            reviewed_by=row["reviewed_by"],
        )

    @staticmethod
    def _to_account(row: Any | None) -> AccountRecord | None:
        if row is None:
            return None
        return AccountRecord(
            id=row["id"],
            display_name=row["display_name"],
            email=row["email"],
            password_hash=row["password_hash"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )
