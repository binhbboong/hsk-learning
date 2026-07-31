from dataclasses import dataclass, field
from typing import Any, Protocol

from hsk_api.content.learning_path import CHECKPOINT, LESSONS, PATH
from hsk_api.models.account import LearningProfilePayload
from hsk_api.models.learning_loop import (
    Checkpoint,
    DailyPathBundle,
    LearningDaySummary,
    LearningPath,
    MultiActivityLesson,
)
from hsk_api.repositories.accounts import AccountRepository
from hsk_api.services.content_quality import ContentQualityGate


class DailyPathGenerator(Protocol):
    def generate(self, **context: Any) -> DailyPathBundle | dict: ...


class DailyPathNotReadyError(ValueError):
    pass


class DailyPathGenerationError(RuntimeError):
    pass


class LearningJourneyCompleteError(ValueError):
    pass


class DailyPathQuotaError(RuntimeError):
    pass


@dataclass
class DailyPathService:
    repository: AccountRepository
    generator: DailyPathGenerator | None
    quality_gate: ContentQualityGate = field(default_factory=ContentQualityGate)
    account_daily_limit: int = 10
    system_daily_limit: int = 50

    def overview(self, account_id: str | None = None) -> LearningPath:
        if account_id is None:
            return PATH.model_copy(
                update={
                    "days": [
                        LearningDaySummary(
                            day_number=1,
                            level=1,
                            difficulty=1,
                            lesson_start=1,
                            lesson_end=5,
                            lesson_ids=[lesson.id for lesson in LESSONS],
                            checkpoint_id=CHECKPOINT.id,
                            completed_lesson_count=0,
                            checkpoint_completed=False,
                            status="current",
                        )
                    ]
                }
            )
        bundles = self.repository.list_daily_paths(account_id)
        lessons = [
            *PATH.lessons,
            *[
                lesson.model_copy()
                for bundle in bundles
                for lesson in bundle.lessons
            ],
        ]
        latest = bundles[-1] if bundles else None
        current_level = latest.level if latest else 1
        current_path_index = latest.path_index if latest else 1
        checkpoint_start = lessons[-5].number
        profile = self.repository.get_profile(account_id)
        day_sources = [
            (1, 1, 1, LESSONS, CHECKPOINT),
            *[
                (
                    bundle.path_index,
                    bundle.level,
                    bundle.difficulty,
                    bundle.lessons,
                    bundle.checkpoint,
                )
                for bundle in bundles
            ],
        ]
        days = [
            self._day_summary(
                day_number=day_number,
                level=level,
                difficulty=difficulty,
                lessons=day_lessons,
                checkpoint=checkpoint,
                profile=profile,
            )
            for day_number, level, difficulty, day_lessons, checkpoint in day_sources
        ]
        completed_all_levels = (
            current_level == 6
            and all(
                lesson.id in profile.completedLessonIds for lesson in lessons[-5:]
            )
            and self._is_mastered(
                profile,
                self._checkpoint_for(account_id, checkpoint_start),
                [lesson.id for lesson in lessons[-5:]],
            )
        )
        return LearningPath(
            level=current_level,
            lessons=lessons,
            current_level=current_level,
            current_path_index=current_path_index,
            current_day_number=current_path_index,
            current_difficulty=latest.difficulty if latest else 1,
            checkpoint_start=checkpoint_start,
            completed_all_levels=completed_all_levels,
            days=days,
        )

    def lesson(self, account_id: str | None, number: int) -> MultiActivityLesson | None:
        if 1 <= number <= len(LESSONS):
            return LESSONS[number - 1]
        if account_id is None:
            return None
        for bundle in self.repository.list_daily_paths(account_id):
            for lesson in bundle.lessons:
                if lesson.number == number:
                    return lesson
        return None

    def checkpoint(self, account_id: str | None, start: int) -> Checkpoint | None:
        if start == 1:
            return CHECKPOINT
        if account_id is None:
            return None
        return self._checkpoint_for(account_id, start)

    def create_next(self, account_id: str) -> DailyPathBundle:
        bundles = self.repository.list_daily_paths(account_id)
        profile = self.repository.get_profile(account_id)
        if bundles:
            latest_persisted = bundles[-1]
            latest_ids = [lesson.id for lesson in latest_persisted.lessons]
            if not all(
                lesson_id in profile.completedLessonIds for lesson_id in latest_ids
            ):
                return latest_persisted

        next_path_index = len(bundles) + 2
        existing = self.repository.get_daily_path(account_id, next_path_index)
        if existing is not None:
            return existing

        latest_bundle = bundles[-1] if bundles else None
        latest_lessons = latest_bundle.lessons if latest_bundle else LESSONS
        latest_checkpoint = latest_bundle.checkpoint if latest_bundle else CHECKPOINT
        lesson_ids = [lesson.id for lesson in latest_lessons]
        if not all(lesson_id in profile.completedLessonIds for lesson_id in lesson_ids):
            raise DailyPathNotReadyError("Hãy hoàn thành đủ 5 Bài của Ngày hiện tại.")
        checkpoint_rate = self._checkpoint_rate(profile, latest_checkpoint.id)
        if checkpoint_rate is None:
            raise DailyPathNotReadyError("Hãy hoàn thành checkpoint của Ngày hiện tại.")
        retention_rate = self._retention_rate(profile, lesson_ids)
        current_level = latest_bundle.level if latest_bundle else 1
        mastered = checkpoint_rate >= 0.8 and retention_rate >= 0.7
        if current_level == 6 and mastered:
            raise LearningJourneyCompleteError("Bạn đã hoàn thành lộ trình HSK 1–6.")
        next_level = min(6, current_level + 1) if mastered else current_level
        next_difficulty = (
            1
            if next_level != current_level
            else min(5, (latest_bundle.difficulty if latest_bundle else 1) + 1)
        )
        if self.generator is None:
            raise DailyPathGenerationError(
                "Chưa cấu hình AI để tạo Ngày học tiếp theo."
            )
        if (
            self.repository.ai_request_count_today(account_id)
            >= self.account_daily_limit
            or self.repository.ai_request_count_today() >= self.system_daily_limit
        ):
            raise DailyPathQuotaError(
                "Đã đạt giới hạn tạo bài AI hôm nay. Vui lòng quay lại sau."
            )
        start_number = latest_lessons[-1].number + 1
        try:
            generated = self.generator.generate(
                account_id=account_id,
                path_index=next_path_index,
                start_number=start_number,
                level=next_level,
                difficulty=next_difficulty,
                checkpoint_rate=checkpoint_rate,
                retention_rate=retention_rate,
                previous_titles=[lesson.title for lesson in latest_lessons],
                mistake_prompts=[
                    str(item.get("prompt", ""))
                    for item in profile.mistakes[-10:]
                    if item.get("prompt")
                ],
            )
            report, bundle = self.quality_gate.assess(
                generated,
                previous_lessons=latest_lessons,
            )
            usage = getattr(self.generator, "last_usage", {}) or {}
            if not report.passed or bundle is None:
                self.repository.record_ai_usage(
                    account_id=account_id,
                    operation="daily_path",
                    status="quality_failed",
                    input_tokens=int(usage.get("input_tokens", 0)),
                    output_tokens=int(usage.get("output_tokens", 0)),
                )
                payload = (
                    generated.model_dump(mode="json")
                    if isinstance(generated, DailyPathBundle)
                    else generated
                )
                self.repository.save_content_draft(
                    account_id=account_id,
                    path_index=next_path_index,
                    payload=payload,
                    quality=report,
                    status="pending",
                )
                raise DailyPathGenerationError(
                    "Nội dung AI cần được quản trị viên kiểm tra trước khi phát hành."
                )
            self._validate_requested_bundle(
                bundle,
                path_index=next_path_index,
                start_number=start_number,
                level=next_level,
                difficulty=next_difficulty,
            )
            self.repository.record_ai_usage(
                account_id=account_id,
                operation="daily_path",
                status="success",
                input_tokens=int(usage.get("input_tokens", 0)),
                output_tokens=int(usage.get("output_tokens", 0)),
            )
        except Exception as error:
            if isinstance(error, DailyPathGenerationError):
                raise
            usage = getattr(self.generator, "last_usage", {}) or {}
            self.repository.record_ai_usage(
                account_id=account_id,
                operation="daily_path",
                status="failed",
                input_tokens=int(usage.get("input_tokens", 0)),
                output_tokens=int(usage.get("output_tokens", 0)),
            )
            raise DailyPathGenerationError(
                "AI chưa thể tạo Ngày mới. Vui lòng thử lại."
            ) from error
        stored = self.repository.save_daily_path(account_id, bundle)
        self.repository.save_content_draft(
            account_id=account_id,
            path_index=next_path_index,
            payload=bundle.model_dump(mode="json"),
            quality=report,
            status="approved",
        )
        return stored

    def _checkpoint_for(self, account_id: str, start: int) -> Checkpoint | None:
        for bundle in self.repository.list_daily_paths(account_id):
            if bundle.lessons[0].number == start:
                return bundle.checkpoint
        return None

    @staticmethod
    def _day_summary(
        *,
        day_number: int,
        level: int,
        difficulty: int,
        lessons: list[MultiActivityLesson],
        checkpoint: Checkpoint,
        profile: LearningProfilePayload,
    ) -> LearningDaySummary:
        lesson_ids = [lesson.id for lesson in lessons]
        completed_count = sum(
            lesson_id in profile.completedLessonIds for lesson_id in lesson_ids
        )
        checkpoint_completed = any(
            result.get("checkpointId") == checkpoint.id
            for result in profile.checkpointResults
        )
        completed = completed_count == 5 and checkpoint_completed
        return LearningDaySummary(
            day_number=day_number,
            level=level,
            difficulty=difficulty,
            lesson_start=lessons[0].number,
            lesson_end=lessons[-1].number,
            lesson_ids=lesson_ids,
            checkpoint_id=checkpoint.id,
            completed_lesson_count=completed_count,
            checkpoint_completed=checkpoint_completed,
            status="completed" if completed else "current",
        )

    def _is_mastered(
        self,
        profile: LearningProfilePayload,
        checkpoint: Checkpoint | None,
        lesson_ids: list[str],
    ) -> bool:
        if checkpoint is None:
            return False
        rate = self._checkpoint_rate(profile, checkpoint.id)
        return (
            rate is not None
            and rate >= 0.8
            and self._retention_rate(profile, lesson_ids) >= 0.7
        )

    @staticmethod
    def _checkpoint_rate(
        profile: LearningProfilePayload,
        checkpoint_id: str,
    ) -> float | None:
        result = next(
            (
                item
                for item in profile.checkpointResults
                if item.get("checkpointId") == checkpoint_id
            ),
            None,
        )
        if not result or not result.get("total"):
            return None
        return float(result.get("score", 0)) / float(result["total"])

    @staticmethod
    def _retention_rate(
        profile: LearningProfilePayload,
        lesson_ids: list[str],
    ) -> float:
        cards = [
            card
            for card in profile.reviewCards
            if card.get("sourceLessonId") in lesson_ids
        ]
        if not cards:
            return 0.0
        remembered = sum(1 for card in cards if int(card.get("repetitions", 0)) > 0)
        return remembered / len(cards)

    @staticmethod
    def _validate_requested_bundle(
        bundle: DailyPathBundle,
        *,
        path_index: int,
        start_number: int,
        level: int,
        difficulty: int,
    ) -> None:
        if bundle.path_index != path_index:
            raise ValueError("AI returned the wrong path index")
        if bundle.level != level or bundle.difficulty != difficulty:
            raise ValueError("AI returned the wrong HSK level or difficulty")
        if [lesson.number for lesson in bundle.lessons] != list(
            range(start_number, start_number + 5)
        ):
            raise ValueError("AI returned the wrong lesson numbers")
