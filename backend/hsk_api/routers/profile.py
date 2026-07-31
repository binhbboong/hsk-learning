from fastapi import APIRouter, Depends

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
    account: AccountRecord = Depends(get_current_account),
    repository: AccountRepository = Depends(get_repository),
) -> LearningProfilePayload:
    return repository.save_profile(account.id, profile)
