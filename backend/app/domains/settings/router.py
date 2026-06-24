from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.common.responses import ok
from app.db.session import get_db
from app.domains.settings.schemas import (
    AlertSettingRead,
    AlertSettingUpdate,
    AppSettingCreate,
    AppSettingRead,
    AppSettingUpdate,
    NewsKeywordCreate,
    NewsKeywordRead,
    NewsKeywordUpdate,
    ScheduledJobCreate,
    ScheduledJobRead,
    ScheduledJobUpdate,
)
from app.domains.settings.service import (
    create_app_setting,
    create_news_keyword,
    create_scheduled_job,
    delete_news_keyword,
    get_alert_settings,
    get_app_settings,
    get_news_keywords,
    get_scheduled_jobs,
    update_alert_setting,
    update_app_setting,
    update_news_keyword,
    update_scheduled_job,
)

router = APIRouter()


@router.get("")
def summary():
    return ok({"menu": "settings", "description": "수집, 알림, 키워드, 인증 설정"})


@router.get("/app-settings", response_model=list[AppSettingRead])
def list_app_settings(db: Session = Depends(get_db)):
    return get_app_settings(db)


@router.post("/app-settings", response_model=AppSettingRead, status_code=201)
def create_app_setting_item(payload: AppSettingCreate, db: Session = Depends(get_db)):
    return create_app_setting(db, payload)


@router.put("/app-settings/{setting_id}", response_model=AppSettingRead)
def update_app_setting_item(setting_id: int, payload: AppSettingUpdate, db: Session = Depends(get_db)):
    return update_app_setting(db, setting_id, payload)


@router.get("/scheduled-jobs", response_model=list[ScheduledJobRead])
def list_scheduled_jobs(db: Session = Depends(get_db)):
    return get_scheduled_jobs(db)


@router.post("/scheduled-jobs", response_model=ScheduledJobRead, status_code=201)
def create_scheduled_job_item(payload: ScheduledJobCreate, db: Session = Depends(get_db)):
    return create_scheduled_job(db, payload)


@router.put("/scheduled-jobs/{job_id}", response_model=ScheduledJobRead)
def update_scheduled_job_item(job_id: int, payload: ScheduledJobUpdate, db: Session = Depends(get_db)):
    return update_scheduled_job(db, job_id, payload)


@router.get("/news-keywords", response_model=list[NewsKeywordRead])
def list_news_keywords(db: Session = Depends(get_db)):
    return get_news_keywords(db)


@router.post("/news-keywords", response_model=NewsKeywordRead, status_code=201)
def create_news_keyword_item(payload: NewsKeywordCreate, db: Session = Depends(get_db)):
    return create_news_keyword(db, payload)


@router.put("/news-keywords/{keyword_id}", response_model=NewsKeywordRead)
def update_news_keyword_item(keyword_id: int, payload: NewsKeywordUpdate, db: Session = Depends(get_db)):
    return update_news_keyword(db, keyword_id, payload)


@router.delete("/news-keywords/{keyword_id}", status_code=204)
def delete_news_keyword_item(keyword_id: int, db: Session = Depends(get_db)):
    delete_news_keyword(db, keyword_id)
    return Response(status_code=204)


@router.get("/alert-settings", response_model=list[AlertSettingRead])
def list_alert_settings(db: Session = Depends(get_db)):
    return get_alert_settings(db)


@router.put("/alert-settings/{setting_id}", response_model=AlertSettingRead)
def update_alert_setting_item(setting_id: int, payload: AlertSettingUpdate, db: Session = Depends(get_db)):
    return update_alert_setting(db, setting_id, payload)
