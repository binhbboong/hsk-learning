import re
from typing import Any

from pydantic import ValidationError

from hsk_api.models.content_ops import QualityReport
from hsk_api.models.learning_loop import DailyPathBundle, MultiActivityLesson


class ContentQualityGate:
    def assess(
        self,
        payload: dict[str, Any] | DailyPathBundle,
        *,
        previous_lessons: list[MultiActivityLesson],
    ) -> tuple[QualityReport, DailyPathBundle | None]:
        try:
            bundle = DailyPathBundle.model_validate(payload)
        except (ValidationError, TypeError, ValueError) as error:
            return (
                QualityReport(
                    passed=False,
                    codes=["schema"],
                    issues=[f"Nội dung chưa đúng cấu trúc: {error}"],
                ),
                None,
            )

        codes: list[str] = []
        issues: list[str] = []
        previous_goals = {self._normalize(item.goal) for item in previous_lessons}
        current_goals = {self._normalize(item.goal) for item in bundle.lessons}
        goal_overlap = len(previous_goals & current_goals) / max(1, len(current_goals))

        previous_words = {
            self._normalize(word.hanzi)
            for lesson in previous_lessons
            for word in lesson.vocabulary
        }
        current_words = {
            self._normalize(word.hanzi)
            for lesson in bundle.lessons
            for word in lesson.vocabulary
        }
        word_overlap = len(previous_words & current_words) / max(1, len(current_words))

        if goal_overlap >= 0.6 or word_overlap >= 0.8:
            codes.append("duplicate")
            issues.append(
                "Mục tiêu hoặc từ vựng trùng quá nhiều với Ngày gần nhất."
            )

        return QualityReport(passed=not codes, codes=codes, issues=issues), bundle

    @staticmethod
    def _normalize(value: str) -> str:
        return re.sub(r"\s+", " ", value.strip().casefold())

