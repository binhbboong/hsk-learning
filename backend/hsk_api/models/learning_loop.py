from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PathLessonSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    number: int = Field(ge=1)
    title: str
    goal: str
    estimated_minutes: int = Field(ge=5, le=15)


class LearningDaySummary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    day_number: int = Field(ge=1)
    level: int = Field(ge=1, le=6)
    difficulty: int = Field(ge=1, le=5)
    lesson_start: int = Field(ge=1)
    lesson_end: int = Field(ge=5)
    lesson_ids: list[str] = Field(min_length=5, max_length=5)
    checkpoint_id: str
    completed_lesson_count: int = Field(ge=0, le=5)
    checkpoint_completed: bool
    status: Literal["completed", "current"]

    @model_validator(mode="after")
    def validate_day_range(self) -> "LearningDaySummary":
        if self.lesson_end != self.lesson_start + 4:
            raise ValueError("A learning day must cover exactly five lessons")
        if self.status == "completed" and (
            self.completed_lesson_count != 5 or not self.checkpoint_completed
        ):
            raise ValueError("A completed learning day needs five lessons and its checkpoint")
        return self


class LearningPath(BaseModel):
    model_config = ConfigDict(extra="forbid")
    level: int = Field(ge=1, le=6)
    lessons: list[PathLessonSummary] = Field(min_length=5)
    current_level: int = Field(default=1, ge=1, le=6)
    current_path_index: int = Field(default=1, ge=1)
    current_day_number: int = Field(default=1, ge=1)
    current_difficulty: int = Field(default=1, ge=1, le=5)
    checkpoint_start: int = Field(default=1, ge=1)
    completed_all_levels: bool = False
    days: list[LearningDaySummary] = Field(default_factory=list)


class DialogueLine(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    speaker: str
    hanzi: str
    audio_text: str
    pinyin: str
    translation_vi: str


class ChoiceOption(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    text: str


class ListeningActivity(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    audio_text: str
    prompt_vi: str
    options: list[ChoiceOption] = Field(min_length=2)
    correct_option_id: str
    transcript_zh: str
    pinyin: str
    translation_vi: str
    explanation_vi: str


class SentenceOrderActivity(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    prompt_vi: str
    tokens: list[str] = Field(min_length=2)
    correct_tokens: list[str] = Field(min_length=2)
    pinyin: str
    translation_vi: str
    explanation_vi: str


class LessonVocabulary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    hanzi: str
    pinyin: str
    meaning_vi: str


class MultiActivityLesson(PathLessonSummary):
    model_config = ConfigDict(extra="forbid")
    level: int = Field(ge=1, le=6)
    dialogue: list[DialogueLine] = Field(min_length=2)
    listening: ListeningActivity
    sentence_order: SentenceOrderActivity
    vocabulary: list[LessonVocabulary] = Field(min_length=2)
    pronunciation_text: str


class CheckpointQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    kind: Literal["listening", "vocabulary", "sentence-order"]
    prompt_vi: str
    audio_text: str | None = None
    options: list[ChoiceOption] = Field(default_factory=list)
    tokens: list[str] = Field(default_factory=list)
    correct_answer: str
    explanation_vi: str


class Checkpoint(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    title: str
    lesson_ids: list[str] = Field(min_length=5, max_length=5)
    questions: list[CheckpointQuestion] = Field(min_length=3, max_length=3)


class DailyPathBundle(BaseModel):
    model_config = ConfigDict(extra="forbid")
    path_index: int = Field(ge=2)
    level: int = Field(ge=1, le=6)
    difficulty: int = Field(ge=1, le=5)
    lessons: list[MultiActivityLesson] = Field(min_length=5, max_length=5)
    checkpoint: Checkpoint

    @model_validator(mode="after")
    def validate_bundle(self) -> "DailyPathBundle":
        numbers = [lesson.number for lesson in self.lessons]
        expected = list(range(numbers[0], numbers[0] + 5))
        if numbers != expected:
            raise ValueError("Daily path lessons must have five consecutive numbers")
        if any(lesson.level != self.level for lesson in self.lessons):
            raise ValueError("All lessons must match the daily path HSK level")
        if self.checkpoint.lesson_ids != [lesson.id for lesson in self.lessons]:
            raise ValueError("Checkpoint must cover exactly the daily path lessons")
        if len({lesson.goal.strip().casefold() for lesson in self.lessons}) != 5:
            raise ValueError("Daily path lesson goals must be unique")
        return self
