from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Protocol
from zoneinfo import ZoneInfo

import httpx

from hsk_api.models.account import AccountRecord
from hsk_api.models.learning_loop import LearningPath
from hsk_api.repositories.accounts import AccountRepository
from hsk_api.services.daily_paths import DailyPathService


class TelegramSender(Protocol):
    def send_message(self, chat_id: str, text: str) -> None: ...


@dataclass
class TelegramBotClient:
    token: str
    timeout_seconds: float = 10.0

    def send_message(self, chat_id: str, text: str) -> None:
        response = httpx.post(
            f"https://api.telegram.org/bot{self.token}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()


@dataclass
class LearningReminderService:
    repository: AccountRepository
    daily_paths: DailyPathService
    sender: TelegramSender | None
    chat_id: str
    account_email: str
    timezone_name: str = "Asia/Ho_Chi_Minh"
    reminder_start_hour: int = 19
    reminder_start_minute: int = 10
    reminder_interval: timedelta = timedelta(minutes=15)
    clock: Callable[[], datetime] = lambda: datetime.now(UTC)

    @property
    def configured(self) -> bool:
        return bool(self.sender and self.chat_id and self.account_email)

    def run_scheduled_reminder(self) -> str:
        local_now = self.clock().astimezone(ZoneInfo(self.timezone_name))
        reminder_start = local_now.replace(
            hour=self.reminder_start_hour,
            minute=self.reminder_start_minute,
            second=0,
            microsecond=0,
        )
        if local_now < reminder_start:
            return "outside_reminder_window"
        if not self.configured:
            return "not_configured"
        account = self.repository.find_by_email(self.account_email)
        if account is None:
            return "account_not_found"
        current_day = self.daily_paths.overview(account.id).days[-1]
        if current_day.status == "completed":
            return "already_completed"
        delivery_at = local_now.astimezone(UTC)
        reminder_date = local_now.date().isoformat()
        if not self.repository.claim_reminder_delivery(
            account.id,
            reminder_date,
            delivery_at,
            self.reminder_interval,
        ):
            return "cooldown_active"
        message = (
            f"⏰ Bạn chưa hoàn thành lộ trình Ngày {current_day.day_number}. "
            f"Tiến độ hiện tại: {current_day.completed_lesson_count}/5 bài, "
            f"từ vựng chủ đề: {'xong' if current_day.topic_vocabulary_completed else 'chưa xong'}, "
            f"checkpoint: {'xong' if current_day.checkpoint_completed else 'chưa xong'}."
        )
        if self._send(message):
            return "reminder_sent"
        self.repository.release_reminder_delivery(
            account.id,
            reminder_date,
            delivery_at,
        )
        return "delivery_failed"

    def send_progress_summary(self) -> str:
        if not self.configured:
            return "not_configured"
        account = self.repository.find_by_email(self.account_email)
        if account is None:
            return "account_not_found"
        current_day = self.daily_paths.overview(account.id).days[-1]
        completed = current_day.status == "completed"
        message = "\n".join(
            [
                "📊 TIẾN ĐỘ HỌC HSK HÔM NAY",
                "",
                f"Tài khoản: {account.email}",
                f"Lộ trình: Ngày {current_day.day_number} · HSK {current_day.level}",
                "",
                f"📚 Bài học: {current_day.completed_lesson_count}/5",
                (
                    "🧠 Từ vựng chủ đề: "
                    + (
                        "Đã hoàn thành"
                        if current_day.topic_vocabulary_completed
                        else "Chưa hoàn thành"
                    )
                ),
                (
                    "✅ Checkpoint: "
                    + (
                        "Đã hoàn thành"
                        if current_day.checkpoint_completed
                        else "Chưa hoàn thành"
                    )
                ),
                "",
                (
                    "🎉 Bạn đã hoàn thành tiến độ hôm nay!"
                    if completed
                    else "⏳ Bạn chưa hoàn thành tiến độ hôm nay."
                ),
            ]
        )
        return "progress_sent" if self._send(message) else "delivery_failed"

    def notify_completion(
        self,
        account: AccountRecord,
        before: LearningPath,
        after: LearningPath,
    ) -> None:
        if not self.configured or account.email.casefold() != self.account_email.casefold():
            return
        before_days = {day.day_number: day for day in before.days}
        for day in after.days:
            previous = before_days.get(day.day_number)
            if previous and previous.status != "completed" and day.status == "completed":
                self._send(
                    f"🎉 Chúc mừng! Bạn đã hoàn thành lộ trình Ngày {day.day_number} "
                    f"(HSK {day.level})."
                )

    def _send(self, message: str) -> bool:
        try:
            assert self.sender is not None
            self.sender.send_message(self.chat_id, message)
            return True
        except (httpx.HTTPError, RuntimeError, OSError):
            return False
