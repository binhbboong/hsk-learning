from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status

from hsk_api.auth.dependencies import get_current_account, get_optional_current_account
from hsk_api.models.account import AccountRecord
from hsk_api.models.learning_loop import (
    Checkpoint,
    DailyPathBundle,
    LearningPath,
    MultiActivityLesson,
)
from hsk_api.services.daily_paths import (
    DailyPathGenerationError,
    DailyPathNotReadyError,
    DailyPathQuotaError,
    DailyPathService,
    LearningJourneyCompleteError,
    LevelExamRequiredError,
)


router = APIRouter(prefix="/api/v1/path", tags=["learning-path"])


def get_daily_path_service(request: Request) -> DailyPathService:
    return request.app.state.daily_path_service


@router.get("", response_model=LearningPath)
def learning_path(
    level: Annotated[int, Query(ge=1, le=6)] = 1,
    account: AccountRecord | None = Depends(get_optional_current_account),
    service: DailyPathService = Depends(get_daily_path_service),
) -> LearningPath:
    del level
    return service.overview(account.id if account else None)


@router.get("/lessons/{number}", response_model=MultiActivityLesson)
def lesson(
    number: Annotated[int, Path(ge=1)],
    account: AccountRecord | None = Depends(get_optional_current_account),
    service: DailyPathService = Depends(get_daily_path_service),
) -> MultiActivityLesson:
    result = service.lesson(account.id if account else None, number)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy bài học.",
        )
    return result


@router.get("/checkpoint", response_model=Checkpoint)
def checkpoint(
    start: Annotated[int, Query(ge=1)] = 1,
    account: AccountRecord | None = Depends(get_optional_current_account),
    service: DailyPathService = Depends(get_daily_path_service),
) -> Checkpoint:
    result = service.checkpoint(account.id if account else None, start)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy checkpoint.",
        )
    return result


@router.post("/next", response_model=DailyPathBundle)
def create_next_path(
    account: AccountRecord = Depends(get_current_account),
    service: DailyPathService = Depends(get_daily_path_service),
) -> DailyPathBundle:
    try:
        return service.create_next(account.id)
    except (DailyPathNotReadyError, LearningJourneyCompleteError, LevelExamRequiredError) as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except DailyPathQuotaError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(exc),
        ) from exc
    except DailyPathGenerationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
