from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import AlertSetting, AppSetting, NewsKeywordSetting, ScheduledJob
from app.domains.settings import repository
from app.domains.settings.schemas import (
    AlertSettingUpdate,
    AppSettingCreate,
    AppSettingUpdate,
    NewsKeywordCreate,
    NewsKeywordUpdate,
    ScheduledJobCreate,
    ScheduledJobUpdate,
)


def _apply_updates(instance, payload) -> None:
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(instance, key, value)


def get_app_settings(db: Session):
    return repository.list_app_settings(db)


def create_app_setting(db: Session, payload: AppSettingCreate):
    if repository.get_app_setting_by_key(db, payload.setting_key):
        raise HTTPException(status_code=409, detail="setting_key already exists")
    item = AppSetting(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_app_setting(db: Session, setting_id: int, payload: AppSettingUpdate):
    item = repository.get_app_setting(db, setting_id)
    if not item:
        raise HTTPException(status_code=404, detail="app setting not found")
    _apply_updates(item, payload)
    db.commit()
    db.refresh(item)
    return item


def get_scheduled_jobs(db: Session):
    return repository.list_scheduled_jobs(db)


def create_scheduled_job(db: Session, payload: ScheduledJobCreate):
    if repository.get_scheduled_job_by_key(db, payload.job_key):
        raise HTTPException(status_code=409, detail="job_key already exists")
    item = ScheduledJob(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_scheduled_job(db: Session, job_id: int, payload: ScheduledJobUpdate):
    item = repository.get_scheduled_job(db, job_id)
    if not item:
        raise HTTPException(status_code=404, detail="scheduled job not found")
    _apply_updates(item, payload)
    db.commit()
    db.refresh(item)
    return item


def get_news_keywords(db: Session):
    return repository.list_news_keywords(db)


def create_news_keyword(db: Session, payload: NewsKeywordCreate):
    if repository.get_news_keyword_by_group_and_keyword(db, payload.group_type, payload.keyword):
        raise HTTPException(status_code=409, detail="keyword already exists in group")
    item = NewsKeywordSetting(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_news_keyword(db: Session, keyword_id: int, payload: NewsKeywordUpdate):
    item = repository.get_news_keyword(db, keyword_id)
    if not item:
        raise HTTPException(status_code=404, detail="news keyword not found")
    _apply_updates(item, payload)
    db.commit()
    db.refresh(item)
    return item


def delete_news_keyword(db: Session, keyword_id: int) -> None:
    item = repository.get_news_keyword(db, keyword_id)
    if not item:
        raise HTTPException(status_code=404, detail="news keyword not found")
    db.delete(item)
    db.commit()


def get_alert_settings(db: Session):
    return repository.list_alert_settings(db)


def update_alert_setting(db: Session, setting_id: int, payload: AlertSettingUpdate):
    item = repository.get_alert_setting(db, setting_id)
    if not item:
        raise HTTPException(status_code=404, detail="alert setting not found")
    _apply_updates(item, payload)
    db.commit()
    db.refresh(item)
    return item
