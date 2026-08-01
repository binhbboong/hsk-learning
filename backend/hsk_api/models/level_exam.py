from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from hsk_api.models.learning_loop import ChoiceOption


LevelExamSkill = Literal["vocabulary", "grammar", "reading", "listening"]


class LevelExamQuestion(BaseModel):
    id: str
    skill: LevelExamSkill
    prompt_vi: str
    options: list[ChoiceOption] = Field(min_length=4, max_length=4)
    correct_option_id: str
    audio_text: str | None = None


class LevelExamPublicQuestion(BaseModel):
    id: str
    skill: LevelExamSkill
    prompt_vi: str
    options: list[ChoiceOption]


class LevelExamDefinition(BaseModel):
    id: str
    account_id: str
    level: int = Field(ge=1, le=6)
    source_path_index: int = Field(ge=1)
    questions: list[LevelExamQuestion] = Field(min_length=20, max_length=20)
    created_at: datetime


class LevelExamSkillResult(BaseModel):
    skill: LevelExamSkill
    correct: int
    total: int = 5
    percent: int


class LevelExamResult(BaseModel):
    level: int
    correct: int
    total: int = 20
    overall_percent: int
    passed: bool
    skills: list[LevelExamSkillResult]
    completed_at: datetime


class LevelExamAttemptRecord(BaseModel):
    id: str
    account_id: str
    exam_id: str
    level: int
    status: Literal["in_progress", "completed"] = "in_progress"
    question_order: list[str]
    selections: dict[str, str] = Field(default_factory=dict)
    flagged_question_ids: list[str] = Field(default_factory=list)
    current_index: int = 0
    started_at: datetime
    completed_at: datetime | None = None
    result: LevelExamResult | None = None


class LevelExamAttemptResponse(BaseModel):
    attempt_id: str
    exam_id: str
    level: int
    status: Literal["in_progress", "completed"]
    questions: list[LevelExamPublicQuestion]
    selections: dict[str, str]
    flagged_question_ids: list[str]
    current_index: int
    started_at: datetime
    result: LevelExamResult | None = None


class LevelExamSaveRequest(BaseModel):
    question_id: str
    option_id: str
    flagged: bool = False
    current_index: int = Field(ge=0, le=19)


class LevelExamStatusResponse(BaseModel):
    eligible: bool
    level: int = Field(ge=1, le=6)
    passed: bool = False
    in_progress: LevelExamAttemptResponse | None = None
    latest_result: LevelExamResult | None = None
    reason_vi: str
