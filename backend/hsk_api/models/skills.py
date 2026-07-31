from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SkillSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["vocabulary", "grammar", "listening", "pronunciation"]
    title: str = Field(min_length=1)
    goal: str = Field(min_length=1)
    estimated_minutes: int = Field(ge=3, le=10)
    route: str = Field(pattern=r"^/")


class SkillCatalog(BaseModel):
    model_config = ConfigDict(extra="forbid")

    level: Literal[1]
    items: list[SkillSummary] = Field(min_length=4, max_length=4)


class ChineseExample(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hanzi: str = Field(min_length=1)
    pinyin: str = Field(min_length=1)
    meaning_vi: str = Field(min_length=1)


class AnswerOption(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    text: str = Field(min_length=1)


class GrammarQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    prompt_vi: str = Field(min_length=1)
    options: list[AnswerOption] = Field(min_length=2)
    correct_option_id: str = Field(min_length=1)
    explanation_vi: str = Field(min_length=1)


class GrammarLesson(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    level: Literal[1]
    kind: Literal["grammar"]
    title: str
    goal: str
    estimated_minutes: int = Field(ge=3, le=10)
    pattern: str
    explanation_vi: str
    examples: list[ChineseExample] = Field(min_length=2)
    questions: list[GrammarQuestion] = Field(min_length=2)


class ListeningLesson(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    level: Literal[1]
    kind: Literal["listening"]
    title: str
    goal: str
    estimated_minutes: int = Field(ge=3, le=10)
    utterance_zh: str
    pinyin: str
    meaning_vi: str
    question_vi: str
    options: list[AnswerOption] = Field(min_length=2)
    correct_option_id: str
    explanation_vi: str


class PronunciationLesson(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    level: Literal[1]
    kind: Literal["pronunciation"]
    title: str
    goal: str
    estimated_minutes: int = Field(ge=3, le=10)
    hanzi: str
    pinyin: str
    meaning_vi: str
    tone_path: list[str] = Field(min_length=2)
    common_mistake_vi: str
    correction_tip_vi: str
