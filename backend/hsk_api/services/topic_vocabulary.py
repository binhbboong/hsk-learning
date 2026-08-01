from dataclasses import dataclass
from typing import Any, Protocol

from hsk_api.content.topic_vocabulary import curated_recommendations, curated_session
from hsk_api.models.topic_vocabulary import (
    TopicRecommendation,
    TopicRecommendationsResponse,
    TopicVocabularySession,
)
from hsk_api.repositories.accounts import AccountRepository


class TopicVocabularyGenerator(Protocol):
    def recommend(self, **context: Any) -> list[dict] | list[TopicRecommendation]: ...

    def generate_session(self, **context: Any) -> dict | TopicVocabularySession: ...


class TopicNotFoundError(ValueError):
    pass


@dataclass
class TopicVocabularyService:
    repository: AccountRepository
    generator: TopicVocabularyGenerator | None

    def recommendations(
        self,
        account_id: str,
        *,
        refresh: bool = False,
    ) -> TopicRecommendationsResponse:
        previous = self.repository.get_topic_recommendations(account_id)
        if previous is not None and not refresh:
            return self._with_progress(account_id, previous)
        level = self._current_level(account_id)
        result: TopicRecommendationsResponse | None = None
        if self.generator is not None:
            try:
                generated = self.generator.recommend(
                    account_id=account_id,
                    level=level,
                    previous_topic_ids=(
                        [item.id for item in previous.items] if previous else []
                    ),
                    mistakes=self.repository.get_profile(account_id).mistakes[-10:],
                )
                result = TopicRecommendationsResponse(
                    source="ai",
                    items=[TopicRecommendation.model_validate(item) for item in generated],
                )
                if previous and {item.id for item in result.items} == {
                    item.id for item in previous.items
                }:
                    result = None
            # Provider/network errors must never block the curated learning path.
            except Exception:
                result = None
        if result is None:
            curated = curated_recommendations(level)
            if refresh and previous:
                previous_ids = {item.id for item in previous.items}
                unseen = [item for item in curated if item.id not in previous_ids]
                seen = [item for item in curated if item.id in previous_ids]
                curated = [*unseen, *seen]
            result = TopicRecommendationsResponse(
                source="curated",
                items=curated if refresh and previous else curated[:7],
            )
        self.repository.save_topic_recommendations(account_id, result)
        return self._with_progress(account_id, result)

    def session(self, account_id: str, topic_id: str) -> TopicVocabularySession:
        stored = self.repository.get_topic_session(account_id, topic_id)
        if stored is not None:
            return stored
        recommendations = self.recommendations(account_id)
        topic = next((item for item in recommendations.items if item.id == topic_id), None)
        if topic is None:
            curated = next(
                (item for item in curated_recommendations(self._current_level(account_id)) if item.id == topic_id),
                None,
            )
            topic = curated
        if topic is None:
            raise TopicNotFoundError("Không tìm thấy chủ đề được đề xuất.")
        generated_session: TopicVocabularySession | None = None
        if self.generator is not None:
            try:
                raw = self.generator.generate_session(
                    account_id=account_id,
                    topic_id=topic.id,
                    topic_name_vi=topic.name_vi,
                    level=topic.level,
                )
                generated_session = TopicVocabularySession.model_validate(raw)
            # Invalid provider output and transport failures share the same safe fallback.
            except Exception:
                generated_session = None
        if generated_session is None:
            generated_session = curated_session(
                topic.id,
                topic.level,
                topic.name_vi,
            )
        return self.repository.save_topic_session(account_id, generated_session)

    def _current_level(self, account_id: str) -> int:
        paths = self.repository.list_daily_paths(account_id)
        return paths[-1].level if paths else 1

    def _with_progress(
        self,
        account_id: str,
        response: TopicRecommendationsResponse,
    ) -> TopicRecommendationsResponse:
        progress = {
            str(item.get("topicId")): item
            for item in self.repository.get_profile(account_id).topicVocabularyProgress
        }
        return response.model_copy(
            update={
                "items": [
                    item.model_copy(
                        update={
                            "learned_count": min(10, int(progress.get(item.id, {}).get("learnedCount", 0))),
                            "remembered_count": min(10, int(progress.get(item.id, {}).get("rememberedCount", 0))),
                        }
                    )
                    for item in response.items
                ]
            }
        )
