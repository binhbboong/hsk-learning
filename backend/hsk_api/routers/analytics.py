from datetime import date

from fastapi import APIRouter, Depends, Query

from hsk_api.auth.dependencies import get_current_account, get_repository
from hsk_api.models.account import AccountRecord
from hsk_api.models.analytics import LearningInsights
from hsk_api.repositories.accounts import AccountRepository
from hsk_api.services.analytics import LearningAnalyticsService


router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


@router.get("/learning", response_model=LearningInsights)
def learning_insights(
    as_of: date = Query(default_factory=date.today),
    account: AccountRecord = Depends(get_current_account),
    repository: AccountRepository = Depends(get_repository),
) -> LearningInsights:
    return LearningAnalyticsService().build(
        repository.get_profile(account.id),
        as_of=as_of,
    )

