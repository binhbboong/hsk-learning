from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class QualityReport(BaseModel):
    passed: bool
    codes: list[str] = Field(default_factory=list)
    issues: list[str] = Field(default_factory=list)


class ContentDraft(BaseModel):
    id: str
    account_id: str
    path_index: int
    status: Literal["pending", "approved", "rejected"]
    payload: dict[str, Any]
    quality: QualityReport
    created_at: datetime
    updated_at: datetime
    reviewed_by: str | None = None


class ContentEditRequest(BaseModel):
    payload: dict[str, Any]


class UsageSummary(BaseModel):
    date: str
    today_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    account_daily_limit: int
    system_daily_limit: int

