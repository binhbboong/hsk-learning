from typing import Annotated

from fastapi import APIRouter, Query

from hsk_api.models.lesson import LessonResponse
from hsk_api.services.lessons import get_recommended_lesson


router = APIRouter(prefix="/api/v1/lessons", tags=["lessons"])


@router.get("/recommended", response_model=LessonResponse)
def recommended_lesson(
    level: Annotated[int, Query(ge=1, le=1)] = 1,
    size: Annotated[int, Query(ge=5, le=5)] = 5,
) -> LessonResponse:
    del level, size
    return get_recommended_lesson()
