from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


PlacementSkill = Literal["vocabulary", "grammar", "listening", "pronunciation"]


class PlacementOption(BaseModel):
    id: str
    text: str


class PlacementQuestion(BaseModel):
    id: str
    skill: PlacementSkill
    level: int = Field(ge=1, le=6)
    prompt_vi: str
    options: list[PlacementOption] = Field(default_factory=list)
    target_text: str | None = None
    target_pinyin: str | None = None
    number: int = Field(ge=1, le=20)
    total: int = 20


class PlacementAnswerRequest(BaseModel):
    option_id: str | None = None
    skip: bool = False


class PlacementAnswerRecord(BaseModel):
    question_id: str
    skill: PlacementSkill
    level: int
    correct: bool | None
    score: int | None = None


class PlacementSkillResult(BaseModel):
    skill: PlacementSkill
    estimated_level: int = Field(ge=1, le=6)
    correct: int = 0
    assessed: int = 0


class PlacementResult(BaseModel):
    recommended_level: int = Field(ge=1, le=6)
    confidence: Literal["low", "medium", "high"]
    confidence_vi: str
    summary_vi: str
    skills: list[PlacementSkillResult]
    completed_at: datetime
    advisory_only: bool = False
    disclaimer_vi: str = "Kết quả chỉ là gợi ý học tập, không phải điểm thi HSK chính thức."


class PlacementAttemptRecord(BaseModel):
    id: str
    account_id: str
    status: Literal["in_progress", "completed"] = "in_progress"
    target_levels: dict[str, int] = Field(default_factory=dict)
    used_question_ids: list[str] = Field(default_factory=list)
    answers: list[PlacementAnswerRecord] = Field(default_factory=list)
    current_question_id: str | None = None
    result: PlacementResult | None = None
    started_at: datetime
    completed_at: datetime | None = None


class PlacementAttemptResponse(BaseModel):
    attempt_id: str
    status: Literal["in_progress", "completed"]
    question: PlacementQuestion | None = None
    result: PlacementResult | None = None


class PlacementStatusResponse(BaseModel):
    can_take: bool
    in_progress: PlacementAttemptResponse | None = None
    latest_result: PlacementResult | None = None
    retake_available_at: datetime | None = None
    selected_level: int | None = None
    can_apply_level: bool = True


class PlacementSelectionRequest(BaseModel):
    selected_level: int = Field(ge=1, le=6)


class PlacementSelectionResponse(BaseModel):
    selected_level: int
    applied: bool = True
