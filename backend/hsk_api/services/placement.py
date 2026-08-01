from datetime import UTC, datetime, timedelta
from uuid import uuid4

from hsk_api.content.placement_test import PLACEMENT_QUESTION_BANK, placement_question
from hsk_api.models.account import LearningProfilePayload
from hsk_api.models.placement import (
    PlacementAnswerRecord,
    PlacementAttemptRecord,
    PlacementAttemptResponse,
    PlacementQuestion,
    PlacementResult,
    PlacementSkillResult,
    PlacementStatusResponse,
)
from hsk_api.repositories.accounts import AccountRepository
from hsk_api.services.daily_paths import DailyPathService


SKILLS = ("vocabulary", "grammar", "listening", "pronunciation")
QUESTIONS_PER_SKILL = 5
RETAKE_DAYS = 30


class PlacementError(ValueError):
    pass


class PlacementService:
    def __init__(self, repository: AccountRepository, daily_paths: DailyPathService | None = None) -> None:
        self.repository = repository
        self.daily_paths = daily_paths

    def status(self, account_id: str) -> PlacementStatusResponse:
        current = self.repository.get_in_progress_placement(account_id)
        latest = self.repository.get_latest_completed_placement(account_id)
        retake_at = latest.completed_at + timedelta(days=RETAKE_DAYS) if latest and latest.completed_at else None
        profile = self.repository.get_profile(account_id)
        return PlacementStatusResponse(
            can_take=latest is None or retake_at is None or datetime.now(UTC) >= retake_at,
            in_progress=self._response(current) if current else None,
            latest_result=latest.result if latest else None,
            retake_available_at=retake_at,
            selected_level=profile.startingLevel,
            can_apply_level=not self._has_learning_progress(profile, account_id),
        )

    def start_or_resume(self, account_id: str) -> tuple[PlacementAttemptResponse, bool]:
        current = self.repository.get_in_progress_placement(account_id)
        if current:
            return self._response(current), False
        status = self.status(account_id)
        if not status.can_take:
            raise PlacementError("Bạn có thể kiểm tra lại sau 30 ngày.")
        attempt = PlacementAttemptRecord(
            id=str(uuid4()), account_id=account_id,
            target_levels={skill: 3 for skill in SKILLS},
            started_at=datetime.now(UTC),
        )
        self._ensure_current_question(attempt)
        return self._response(self.repository.save_placement_attempt(attempt)), True

    def answer(self, account_id: str, attempt_id: str, option_id: str | None, skip: bool = False) -> PlacementAttemptResponse:
        attempt = self._owned_attempt(account_id, attempt_id)
        question = placement_question(attempt.current_question_id or "")
        if question is None:
            raise PlacementError("Không tìm thấy câu hiện tại.")
        if question.skill == "pronunciation" and skip:
            self._record(attempt, question.id, question.skill, question.level, None)
            return self._response(self.repository.save_placement_attempt(attempt))
        if question.skill == "pronunciation":
            raise PlacementError("Câu hiện tại cần bản thu phát âm.")
        if skip:
            correct = None
        elif not option_id or option_id not in {item.id for item in question.options}:
            raise PlacementError("Hãy chọn một đáp án hợp lệ.")
        else:
            correct = option_id == question.correct_option_id
        self._record(attempt, question.id, question.skill, question.level, correct)
        return self._response(self.repository.save_placement_attempt(attempt))

    def record_pronunciation(self, account_id: str, attempt_id: str, score: int | None) -> PlacementAttemptResponse:
        attempt = self._owned_attempt(account_id, attempt_id)
        question = placement_question(attempt.current_question_id or "")
        if question is None or question.skill != "pronunciation":
            raise PlacementError("Câu hiện tại không phải câu phát âm.")
        self._record(attempt, question.id, question.skill, question.level, None if score is None else score >= 70, score)
        return self._response(self.repository.save_placement_attempt(attempt))

    def skip(self, account_id: str) -> int:
        profile = self.repository.get_profile(account_id)
        if self._has_learning_progress(profile, account_id):
            return profile.startingLevel or 1
        profile.startingLevel = 1
        profile.placementTest = {"status": "skipped", "selectedLevel": 1}
        self.repository.save_profile(account_id, profile)
        return 1

    def select_level(self, account_id: str, selected_level: int) -> int:
        profile = self.repository.get_profile(account_id)
        if self._has_learning_progress(profile, account_id):
            raise PlacementError("Lộ trình đã có tiến độ nên kết quả mới chỉ mang tính tham khảo.")
        if selected_level != 1:
            if self.daily_paths is None:
                raise PlacementError("Chưa thể chuẩn bị Ngày 1 cho cấp HSK đã chọn.")
            self.daily_paths.create_initial(account_id, selected_level)
        profile.startingLevel = selected_level
        profile.placementTest = {"status": "applied", "selectedLevel": selected_level}
        self.repository.save_profile(account_id, profile)
        return selected_level

    def _record(self, attempt, question_id, skill, level, correct, score=None) -> None:
        attempt.answers.append(PlacementAnswerRecord(
            question_id=question_id, skill=skill, level=level, correct=correct, score=score,
        ))
        attempt.used_question_ids.append(question_id)
        if correct is not None:
            attempt.target_levels[skill] = max(1, min(6, level + (1 if correct else -1)))
        attempt.current_question_id = None
        if len(attempt.answers) == len(SKILLS) * QUESTIONS_PER_SKILL:
            attempt.status = "completed"
            attempt.completed_at = datetime.now(UTC)
            attempt.result = self._result(attempt)
        else:
            self._ensure_current_question(attempt)

    def _ensure_current_question(self, attempt: PlacementAttemptRecord) -> None:
        if attempt.current_question_id or attempt.status == "completed":
            return
        skill = SKILLS[len(attempt.answers) // QUESTIONS_PER_SKILL]
        target = attempt.target_levels.get(skill, 3)
        available = [q for q in PLACEMENT_QUESTION_BANK if q.skill == skill and q.id not in attempt.used_question_ids]
        chosen = min(available, key=lambda q: (abs(q.level - target), q.level))
        attempt.current_question_id = chosen.id

    def _response(self, attempt: PlacementAttemptRecord) -> PlacementAttemptResponse:
        public = None
        definition = placement_question(attempt.current_question_id or "")
        if definition:
            public = PlacementQuestion(
                id=definition.id, skill=definition.skill, level=definition.level,
                prompt_vi=definition.prompt_vi, options=list(definition.options),
                target_text=definition.target_text, target_pinyin=definition.target_pinyin,
                number=len(attempt.answers) + 1,
            )
        return PlacementAttemptResponse(
            attempt_id=attempt.id, status=attempt.status, question=public, result=attempt.result,
        )

    def _result(self, attempt: PlacementAttemptRecord) -> PlacementResult:
        skill_results = []
        assessed_total = 0
        for skill in SKILLS:
            answers = [item for item in attempt.answers if item.skill == skill]
            assessed = [item for item in answers if item.correct is not None]
            assessed_total += len(assessed)
            estimates = [max(1, min(6, item.level + (1 if item.correct else -1))) for item in assessed]
            level = max(1, min(6, round(sum(estimates) / len(estimates)))) if estimates else 1
            skill_results.append(PlacementSkillResult(
                skill=skill, estimated_level=level,
                correct=sum(item.correct is True for item in assessed), assessed=len(assessed),
            ))
        recommended = max(1, min(6, round(sum(item.estimated_level for item in skill_results) / 4)))
        confidence = "high" if assessed_total == 20 else "medium" if assessed_total >= 15 else "low"
        labels = {"high": "Cao", "medium": "Khá", "low": "Thấp"}
        return PlacementResult(
            recommended_level=recommended, confidence=confidence,
            confidence_vi=labels[confidence],
            summary_vi=f"Bạn nên bắt đầu ở HSK {recommended} và củng cố kỹ năng có ước lượng thấp nhất.",
            skills=skill_results, completed_at=attempt.completed_at or datetime.now(UTC),
            advisory_only=self._has_learning_progress(self.repository.get_profile(attempt.account_id), attempt.account_id),
        )

    def _owned_attempt(self, account_id: str, attempt_id: str) -> PlacementAttemptRecord:
        attempt = self.repository.get_placement_attempt(attempt_id)
        if attempt is None or attempt.account_id != account_id or attempt.status != "in_progress":
            raise PlacementError("Không tìm thấy lượt kiểm tra đang làm.")
        return attempt

    def _has_learning_progress(self, profile: LearningProfilePayload, account_id: str) -> bool:
        return bool(profile.completedLessonIds or profile.checkpointResults or self.repository.list_daily_paths(account_id))
