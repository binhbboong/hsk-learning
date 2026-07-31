from typing import Literal
from pydantic import BaseModel, Field


class SyllableFeedback(BaseModel):
    target: str
    tone: int = Field(ge=0, le=4)
    status: Literal["good", "review", "uncertain"]
    heard: str = ""
    tip_vi: str


class PronunciationResult(BaseModel):
    verdict: Literal["correct", "needs_practice"]
    score: int = Field(ge=0, le=100)
    content_score: int = Field(default=0, ge=0, le=100)
    transcript: str
    feedback_vi: str
    focus_vi: list[str] = []
    syllables: list[SyllableFeedback] = Field(default_factory=list)
    disclaimer_vi: str = (
        "Phản hồi AI chỉ hỗ trợ luyện tập, không phải điểm thi hay đánh giá của giáo viên."
    )


class SpeechSampleRequest(BaseModel):
    text: str = Field(min_length=1, max_length=500)
    speed: float = Field(default=0.82, ge=0.5, le=1.5)
