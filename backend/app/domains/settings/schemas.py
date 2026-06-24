from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class AppSettingBase(BaseModel):
    setting_key: str
    setting_value: str | None = None
    value_type: str = "string"
    description: str | None = None


class AppSettingCreate(AppSettingBase):
    pass


class AppSettingUpdate(BaseModel):
    setting_value: str | None = None
    value_type: str | None = None
    description: str | None = None


class AppSettingRead(AppSettingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ScheduledJobBase(BaseModel):
    job_key: str
    job_name: str
    enabled: bool = True
    schedule_type: str
    cron_expression: str | None = None
    config_json: dict[str, Any] | None = None


class ScheduledJobCreate(ScheduledJobBase):
    pass


class ScheduledJobUpdate(BaseModel):
    job_name: str | None = None
    enabled: bool | None = None
    schedule_type: str | None = None
    cron_expression: str | None = None
    config_json: dict[str, Any] | None = None


class ScheduledJobRead(ScheduledJobBase):
    id: int
    last_run_at: datetime | None = None
    next_run_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NewsKeywordBase(BaseModel):
    group_type: str
    keyword: str
    weight: int = 1
    enabled: bool = True
    is_default: bool = False


class NewsKeywordCreate(NewsKeywordBase):
    pass


class NewsKeywordUpdate(BaseModel):
    group_type: str | None = None
    keyword: str | None = None
    weight: int | None = None
    enabled: bool | None = None
    is_default: bool | None = None


class NewsKeywordRead(NewsKeywordBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertSettingUpdate(BaseModel):
    enabled: bool | None = None
    news_alert_enabled: bool | None = None
    price_alert_enabled: bool | None = None
    target_scope: str | None = None
    min_importance_score: int | None = None
    min_duplicate_count: int | None = None
    min_source_count: int | None = None
    event_types_json: list[str] | None = None
    keyword_groups_json: list[str] | None = None
    max_daily_alerts: int | None = None
    max_hourly_alerts: int | None = None
    send_email: bool | None = None


class AlertSettingRead(AlertSettingUpdate):
    id: int
    enabled: bool
    news_alert_enabled: bool
    price_alert_enabled: bool
    target_scope: str
    min_importance_score: int
    min_duplicate_count: int
    min_source_count: int
    max_daily_alerts: int
    max_hourly_alerts: int
    send_email: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
