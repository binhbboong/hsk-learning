from datetime import datetime
from typing import Literal

import re

from pydantic import BaseModel, Field, field_validator


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class RegisterRequest(BaseModel):
    display_name: str = Field(min_length=2, max_length=60)
    email: str
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def valid_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not EMAIL_PATTERN.fullmatch(normalized):
            raise ValueError("Email không hợp lệ.")
        return normalized


class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=1, max_length=128)

    @field_validator("email")
    @classmethod
    def valid_email(cls, value: str) -> str:
        return RegisterRequest.valid_email(value)


class UserResponse(BaseModel):
    id: str
    display_name: str
    email: str
    is_admin: bool = False


class SessionResponse(BaseModel):
    token: str
    user: UserResponse


class LearningPreferences(BaseModel):
    goal: Literal["communication", "travel", "work", "exam", "culture"] = "communication"
    dailyMinutes: Literal[10, 20, 30] = 20
    preferredTopics: list[Literal[
        "food", "transport", "shopping", "family", "workplace", "hobbies",
    ]] = Field(default_factory=list, max_length=3)


class LearningProfilePayload(BaseModel):
    version: int = 1
    completedLessonIds: list[str] = Field(default_factory=list)
    streak: dict = Field(default_factory=dict)
    reviewCards: list[dict] = Field(default_factory=list)
    mistakes: list[dict] = Field(default_factory=list)
    notebook: list[dict] = Field(default_factory=list)
    checkpointResults: list[dict] = Field(default_factory=list)
    activityEvents: list[dict] = Field(default_factory=list)
    topicVocabularyProgress: list[dict] = Field(default_factory=list)
    startingLevel: int | None = Field(default=None, ge=1, le=6)
    placementTest: dict | None = None
    learningPreferences: LearningPreferences | None = None


class AccountRecord(BaseModel):
    id: str
    display_name: str
    email: str
    password_hash: str
    created_at: datetime
