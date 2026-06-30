from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


TAG_TARGET_TYPES = ("stock", "trade", "news", "memo")


class TagCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    color: str | None = Field(default=None, max_length=20)
    tag_type: str = Field(min_length=1, max_length=30)


class TagUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    color: str | None = Field(default=None, max_length=20)
    tag_type: str | None = Field(default=None, min_length=1, max_length=30)


class TagRead(BaseModel):
    id: int
    name: str
    color: str | None = None
    tag_type: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TagLinkCreate(BaseModel):
    tag_id: int
    target_type: str = Field(min_length=1, max_length=30)
    target_id: int


class TagLinkRead(BaseModel):
    id: int
    tag_id: int
    target_type: str
    target_id: int
    created_at: datetime
    tag_name: str
    tag_color: str | None = None
    tag_type: str
