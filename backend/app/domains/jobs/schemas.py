from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class JobRead(BaseModel):
    id: int
    job_key: str
    job_name: str
    enabled: bool
    schedule_type: str
    cron_expression: str | None = None
    config_json: dict[str, Any] | None = None
    last_run_at: datetime | None = None
    next_run_at: datetime | None = None
    last_status: str | None = None
    last_message: str | None = None
    last_started_at: datetime | None = None
    last_finished_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class JobRunRequest(BaseModel):
    dry_run: bool | None = None
    config_json: dict[str, Any] | None = None


class JobBatchRunRequest(BaseModel):
    job_ids: list[int] | None = None
    dry_run: bool | None = None
    config_json: dict[str, Any] | None = None


class JobRunResult(BaseModel):
    job_id: int
    job_key: str
    status: str
    started_at: datetime
    finished_at: datetime
    message: str
    result: dict[str, Any] = Field(default_factory=dict)


class JobSummary(BaseModel):
    total_count: int
    enabled_count: int
    disabled_count: int
    success_count: int
    failed_count: int
    never_run_count: int
    recent_runs: list[JobRunResult]

