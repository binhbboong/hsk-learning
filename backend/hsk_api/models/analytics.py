from typing import Literal

from pydantic import BaseModel, Field


class ActivityDay(BaseModel):
    date: str
    active: bool
    count: int = Field(ge=0)


class RetentionWindow(BaseModel):
    rate: float | None = Field(default=None, ge=0, le=1)
    sample_size: int = Field(ge=0)
    remembered: int = Field(ge=0)
    label_vi: str


class SkillWeakness(BaseModel):
    skill: Literal["listening", "sentence-order", "vocabulary", "pronunciation"]
    label_vi: str
    evidence_count: int = Field(ge=0)
    severity: float = Field(ge=0)
    reason_vi: str


class LearningRecommendation(BaseModel):
    title: str
    reason_vi: str
    route: str
    query_params: dict[str, str] = Field(default_factory=dict)


class LearningInsights(BaseModel):
    activity_days: list[ActivityDay] = Field(min_length=7, max_length=7)
    retention_30d: RetentionWindow
    weaknesses: list[SkillWeakness]
    recommendation: LearningRecommendation

