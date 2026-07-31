from typing import Annotated, Literal

from fastapi import APIRouter, Query

from hsk_api.content.default_skills import (
    GRAMMAR_LESSON,
    LISTENING_LESSON,
    PRONUNCIATION_LESSON,
    SKILL_CATALOG,
)
from hsk_api.models.skills import (
    GrammarLesson,
    ListeningLesson,
    PronunciationLesson,
    SkillCatalog,
)


router = APIRouter(prefix="/api/v1/skills", tags=["skills"])
HskOne = Annotated[int, Query(ge=1, le=1)]


@router.get("", response_model=SkillCatalog)
def skill_catalog(level: HskOne = 1) -> SkillCatalog:
    del level
    return SKILL_CATALOG


@router.get(
    "/{kind}",
    response_model=GrammarLesson | ListeningLesson | PronunciationLesson,
)
def skill_lesson(
    kind: Literal["grammar", "listening", "pronunciation"],
    level: HskOne = 1,
) -> GrammarLesson | ListeningLesson | PronunciationLesson:
    del level
    return {
        "grammar": GRAMMAR_LESSON,
        "listening": LISTENING_LESSON,
        "pronunciation": PRONUNCIATION_LESSON,
    }[kind]
