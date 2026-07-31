from collections import Counter
from datetime import date, datetime, timedelta

from hsk_api.models.account import LearningProfilePayload
from hsk_api.models.analytics import (
    ActivityDay,
    LearningInsights,
    LearningRecommendation,
    RetentionWindow,
    SkillWeakness,
)


LABELS = {
    "listening": "Nghe",
    "sentence-order": "Sắp xếp câu",
    "vocabulary": "Từ vựng",
    "pronunciation": "Phát âm",
}


class LearningAnalyticsService:
    def build(
        self,
        profile: LearningProfilePayload,
        *,
        as_of: date,
    ) -> LearningInsights:
        event_dates = [
            self._event_date(item.get("occurredAt"))
            for item in profile.activityEvents
        ]
        counts = Counter(item for item in event_dates if item is not None)
        activity_days = [
            ActivityDay(
                date=(day := as_of - timedelta(days=offset)).isoformat(),
                active=counts[day] > 0,
                count=counts[day],
            )
            for offset in range(6, -1, -1)
        ]

        recent_cards = [
            card
            for card in profile.reviewCards
            if self._within_30_days(card.get("lastReviewedAt"), as_of)
        ]
        remembered = sum(
            1 for card in recent_cards if int(card.get("repetitions", 0)) > 0
        )
        sample_size = len(recent_cards)
        retention = RetentionWindow(
            rate=(remembered / sample_size) if sample_size else None,
            sample_size=sample_size,
            remembered=remembered,
            label_vi=(
                f"Nhớ {remembered}/{sample_size} từ trong 30 ngày"
                if sample_size
                else "Chưa đủ dữ liệu ôn trong 30 ngày"
            ),
        )

        evidence = Counter(
            item.get("kind")
            for item in profile.mistakes
            if item.get("kind") in {"listening", "sentence-order"}
        )
        evidence["vocabulary"] += sum(
            1 for card in recent_cards if int(card.get("repetitions", 0)) == 0
        )
        evidence["pronunciation"] += sum(
            1
            for event in profile.activityEvents
            if event.get("kind") == "pronunciation"
            and float(event.get("score", 100)) < 85
        )
        order = ["listening", "sentence-order", "vocabulary", "pronunciation"]
        weaknesses = sorted(
            [
                SkillWeakness(
                    skill=skill,
                    label_vi=LABELS[skill],
                    evidence_count=evidence[skill],
                    severity=float(evidence[skill]),
                    reason_vi=f"Có {evidence[skill]} dấu hiệu cần luyện thêm.",
                )
                for skill in order
                if evidence[skill] > 0
            ],
            key=lambda item: (-item.severity, order.index(item.skill)),
        )

        if weaknesses:
            primary = weaknesses[0]
            if primary.skill in {"listening", "sentence-order"}:
                recommendation = LearningRecommendation(
                    title=f"Ôn lại {primary.label_vi.lower()}",
                    reason_vi=primary.reason_vi,
                    route="/learn/review",
                    query_params={"source": "mistakes"},
                )
            elif primary.skill == "vocabulary":
                recommendation = LearningRecommendation(
                    title="Ôn từ đến hạn",
                    reason_vi=primary.reason_vi,
                    route="/learn/review",
                    query_params={"source": "srs"},
                )
            else:
                recommendation = LearningRecommendation(
                    title="Luyện lại phát âm",
                    reason_vi=primary.reason_vi,
                    route="/learn/lesson/1",
                )
        elif not profile.completedLessonIds:
            recommendation = LearningRecommendation(
                title="Bắt đầu Bài 1",
                reason_vi="Bắt đầu từ HSK 1, độ khó 1 dành cho người mới.",
                route="/learn/lesson/1",
            )
        else:
            recommendation = LearningRecommendation(
                title="Tiếp tục lộ trình",
                reason_vi="Bạn chưa có điểm yếu nổi bật cần ưu tiên.",
                route="/learn",
            )

        return LearningInsights(
            activity_days=activity_days,
            retention_30d=retention,
            weaknesses=weaknesses,
            recommendation=recommendation,
        )

    @staticmethod
    def _event_date(value: object) -> date | None:
        if not isinstance(value, str):
            return None
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        except ValueError:
            return None

    @classmethod
    def _within_30_days(cls, value: object, as_of: date) -> bool:
        reviewed = cls._event_date(value)
        if reviewed is None:
            return True
        return as_of - timedelta(days=29) <= reviewed <= as_of

