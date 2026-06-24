from sqlalchemy.orm import Session

from app.db.models import AlertSetting, AppSetting, NewsKeywordSetting, ScheduledJob


def list_app_settings(db: Session):
    return db.query(AppSetting).order_by(AppSetting.setting_key).all()


def get_app_setting(db: Session, setting_id: int):
    return db.get(AppSetting, setting_id)


def get_app_setting_by_key(db: Session, setting_key: str):
    return db.query(AppSetting).filter(AppSetting.setting_key == setting_key).first()


def list_scheduled_jobs(db: Session):
    return db.query(ScheduledJob).order_by(ScheduledJob.job_key).all()


def get_scheduled_job(db: Session, job_id: int):
    return db.get(ScheduledJob, job_id)


def get_scheduled_job_by_key(db: Session, job_key: str):
    return db.query(ScheduledJob).filter(ScheduledJob.job_key == job_key).first()


def list_news_keywords(db: Session):
    return db.query(NewsKeywordSetting).order_by(
        NewsKeywordSetting.group_type,
        NewsKeywordSetting.keyword,
    ).all()


def get_news_keyword(db: Session, keyword_id: int):
    return db.get(NewsKeywordSetting, keyword_id)


def get_news_keyword_by_group_and_keyword(db: Session, group_type: str, keyword: str):
    return db.query(NewsKeywordSetting).filter(
        NewsKeywordSetting.group_type == group_type,
        NewsKeywordSetting.keyword == keyword,
    ).first()


def list_alert_settings(db: Session):
    return db.query(AlertSetting).order_by(AlertSetting.id).all()


def get_alert_setting(db: Session, setting_id: int):
    return db.get(AlertSetting, setting_id)
