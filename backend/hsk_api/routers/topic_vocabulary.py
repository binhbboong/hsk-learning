from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from hsk_api.auth.dependencies import get_current_account
from hsk_api.models.account import AccountRecord
from hsk_api.models.topic_vocabulary import (
    CreateTopicSessionRequest,
    TopicRecommendationsResponse,
    TopicVocabularySession,
)
from hsk_api.services.topic_vocabulary import (
    TopicNotFoundError,
    TopicVocabularyService,
)


router = APIRouter(prefix="/api/v1/topic-vocabulary", tags=["topic-vocabulary"])


def get_topic_vocabulary_service(request: Request) -> TopicVocabularyService:
    return request.app.state.topic_vocabulary_service


@router.get("/recommendations", response_model=TopicRecommendationsResponse)
def recommendations(
    refresh: bool = Query(default=False),
    account: AccountRecord = Depends(get_current_account),
    service: TopicVocabularyService = Depends(get_topic_vocabulary_service),
) -> TopicRecommendationsResponse:
    return service.recommendations(account.id, refresh=refresh)


@router.post("/sessions", response_model=TopicVocabularySession)
def create_session(
    payload: CreateTopicSessionRequest,
    account: AccountRecord = Depends(get_current_account),
    service: TopicVocabularyService = Depends(get_topic_vocabulary_service),
) -> TopicVocabularySession:
    try:
        return service.session(account.id, payload.topic_id)
    except TopicNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
