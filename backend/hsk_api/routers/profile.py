from fastapi import APIRouter, Depends, Request

from hsk_api.auth.dependencies import get_current_account, get_repository
from hsk_api.models.account import AccountRecord, LearningProfilePayload
from hsk_api.repositories.accounts import AccountRepository


router = APIRouter(prefix="/api/v1/profile", tags=["profile"])


@router.get("", response_model=LearningProfilePayload)
def get_profile(
    account: AccountRecord = Depends(get_current_account),
    repository: AccountRepository = Depends(get_repository),
) -> LearningProfilePayload:
    return repository.get_profile(account.id)


@router.put("", response_model=LearningProfilePayload)
def save_profile(
    profile: LearningProfilePayload,
    request: Request,
    account: AccountRecord = Depends(get_current_account),
    repository: AccountRepository = Depends(get_repository),
) -> LearningProfilePayload:
    daily_paths = request.app.state.daily_path_service
    before = daily_paths.overview(account.id)
    saved = repository.save_profile(account.id, profile)
    after = daily_paths.overview(account.id)
    request.app.state.learning_reminder_service.notify_completion(
        account, before, after,
    )
    return saved
