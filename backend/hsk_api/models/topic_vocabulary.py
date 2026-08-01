from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class TopicRecommendation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(min_length=1, max_length=80)
    name_vi: str = Field(min_length=2, max_length=80)
    description_vi: str = Field(min_length=5, max_length=240)
    reason_vi: str = Field(min_length=5, max_length=240)
    word_count: int = Field(default=10, ge=10, le=10)
    level: int = Field(ge=1, le=6)
    learned_count: int = Field(default=0, ge=0, le=10)
    remembered_count: int = Field(default=0, ge=0, le=10)


class TopicRecommendationsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source: Literal["ai", "curated"]
    items: list[TopicRecommendation] = Field(min_length=5)

    @model_validator(mode="after")
    def unique_topics(self) -> "TopicRecommendationsResponse":
        ids = [item.id for item in self.items]
        if len(ids) != len(set(ids)):
            raise ValueError("Topic recommendations must be unique")
        return self


class TopicVocabularyWord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(min_length=1, max_length=80)
    hanzi: str = Field(min_length=1, max_length=16)
    pinyin: str = Field(min_length=1, max_length=80)
    sino_vietnamese: str = Field(min_length=1, max_length=80)
    meaning_vi: str = Field(min_length=1, max_length=160)
    example_zh: str = Field(min_length=2, max_length=240)
    example_vi: str = Field(min_length=2, max_length=240)
    audio_text: str = ""
    example_audio_text: str = ""
    is_extension: bool = False

    @model_validator(mode="after")
    def default_audio_text(self) -> "TopicVocabularyWord":
        if not self.audio_text:
            self.audio_text = self.hanzi
        if not self.example_audio_text:
            self.example_audio_text = self.example_zh
        return self


class TopicVocabularySession(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(min_length=1, max_length=120)
    topic_id: str = Field(min_length=1, max_length=80)
    topic_name_vi: str = Field(min_length=2, max_length=80)
    level: int = Field(ge=1, le=6)
    source: Literal["ai", "curated"]
    words: list[TopicVocabularyWord] = Field(min_length=10, max_length=10)

    @model_validator(mode="after")
    def exactly_ten_unique_words(self) -> "TopicVocabularySession":
        ids = [word.id.casefold() for word in self.words]
        hanzi = [word.hanzi.strip() for word in self.words]
        if len(set(ids)) != 10 or len(set(hanzi)) != 10:
            raise ValueError("A topic session needs ten unique words")
        return self


class CreateTopicSessionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    topic_id: str = Field(min_length=1, max_length=80)
