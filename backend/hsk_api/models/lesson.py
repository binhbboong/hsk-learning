from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class VocabularyCard(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    hanzi: str = Field(min_length=1)
    pinyin: str = Field(min_length=1)
    sino_vietnamese: str = Field(min_length=1)
    meaning_vi: str = Field(min_length=1)
    example_zh: str = Field(min_length=1)
    example_vi: str = Field(min_length=1)


class Lesson(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    level: Literal[1]
    title: str = Field(min_length=1)
    goal: str = Field(min_length=1)
    estimated_minutes: int = Field(ge=1, le=15)
    cards: list[VocabularyCard] = Field(min_length=5, max_length=5)


class LessonResponse(Lesson):
    source: Literal["ai", "fallback"]
