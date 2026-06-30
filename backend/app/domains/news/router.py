from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.domains.news.schemas import (
    AlertCandidateItem,
    AlertCandidateRecalculateResult,
    AlertCandidateSummary,
    AlertHistoryRead,
    AlertHistorySummary,
    AlertSendRequest,
    AlertSendResult,
    GptRunRequest,
    GptRunResult,
    GptStatusSummary,
    GptTargetsSummary,
    MarketNewsCollectRequest,
    NewsReviewItem,
    NewsReviewUpdate,
    NewsCollectJobRead,
    NewsRead,
    NewsSummary,
)
from app.domains.news.service import (
    collect_market_news,
    get_alert_candidates,
    get_alert_histories,
    get_alert_histories_summary,
    get_alert_summary,
    get_collect_job_detail,
    get_collect_jobs,
    get_gpt_review_list,
    get_gpt_status,
    get_gpt_targets,
    get_news_detail,
    get_news_list,
    get_news_summary,
    recalculate_alert_candidates,
    dry_run_send_alerts,
    send_alerts,
    run_gpt_filter,
    run_gpt_summary,
    update_gpt_review,
)
from app.domains.trades.schemas import NewsTradeRead
from app.domains.trades.service import get_news_related_trades

router = APIRouter()


@router.get("", response_model=list[NewsRead])
def list_items(
    keyword: str | None = None,
    stock_code: str | None = None,
    market_scope: str | None = None,
    event_type: str | None = None,
    filter_status: str | None = None,
    min_importance_score: int | None = None,
    is_alert_target: bool | None = None,
    is_gpt_summary_target: bool | None = None,
    gpt_summary_status: str | None = None,
    gpt_filter_result: str | None = None,
    published_from: datetime | None = None,
    published_to: datetime | None = None,
    db: Session = Depends(get_db),
):
    return get_news_list(
        db=db,
        keyword=keyword,
        stock_code=stock_code,
        market_scope=market_scope,
        event_type=event_type,
        filter_status=filter_status,
        min_importance_score=min_importance_score,
        is_alert_target=is_alert_target,
        is_gpt_summary_target=is_gpt_summary_target,
        gpt_summary_status=gpt_summary_status,
        gpt_filter_result=gpt_filter_result,
        published_from=published_from,
        published_to=published_to,
    )


@router.get("/summary", response_model=NewsSummary)
def summary(db: Session = Depends(get_db)):
    return get_news_summary(db)


@router.post("/collect/market", response_model=NewsCollectJobRead)
def collect_market(payload: MarketNewsCollectRequest, db: Session = Depends(get_db)):
    return collect_market_news(db, payload)


@router.get("/collect/jobs", response_model=list[NewsCollectJobRead])
def list_jobs(db: Session = Depends(get_db)):
    return get_collect_jobs(db)


@router.get("/collect/jobs/{job_id}", response_model=NewsCollectJobRead)
def detail_job(job_id: int, db: Session = Depends(get_db)):
    return get_collect_job_detail(db, job_id)


@router.post("/gpt/summary/run", response_model=GptRunResult)
def run_summary(payload: GptRunRequest, db: Session = Depends(get_db)):
    return run_gpt_summary(db, payload)


@router.post("/gpt/filter/run", response_model=GptRunResult)
def run_filter(payload: GptRunRequest, db: Session = Depends(get_db)):
    return run_gpt_filter(db, payload)


@router.get("/gpt/targets", response_model=GptTargetsSummary)
def gpt_targets(db: Session = Depends(get_db)):
    return get_gpt_targets(db)


@router.get("/gpt/status", response_model=GptStatusSummary)
def gpt_status(db: Session = Depends(get_db)):
    return get_gpt_status(db)


@router.get("/gpt/review", response_model=list[NewsReviewItem])
def gpt_review(
    gpt_summary_status: str | None = None,
    gpt_filter_result: str | None = None,
    min_importance_score: int | None = None,
    stock_code: str | None = None,
    keyword: str | None = None,
    published_from: datetime | None = None,
    published_to: datetime | None = None,
    db: Session = Depends(get_db),
):
    return get_gpt_review_list(
        db=db,
        gpt_summary_status=gpt_summary_status,
        gpt_filter_result=gpt_filter_result,
        min_importance_score=min_importance_score,
        stock_code=stock_code,
        keyword=keyword,
        published_from=published_from,
        published_to=published_to,
    )


@router.patch("/gpt/review/{news_id}", response_model=NewsReviewItem)
def patch_gpt_review(news_id: int, payload: NewsReviewUpdate, db: Session = Depends(get_db)):
    return update_gpt_review(db, news_id, payload)


@router.post("/alerts/candidates/recalculate", response_model=AlertCandidateRecalculateResult)
def recalculate_candidates(db: Session = Depends(get_db)):
    return recalculate_alert_candidates(db)


@router.get("/alerts/candidates", response_model=list[AlertCandidateItem])
def alert_candidates(
    stock_code: str | None = None,
    gpt_filter_result: str | None = None,
    min_importance_score: int | None = None,
    published_from: datetime | None = None,
    published_to: datetime | None = None,
    db: Session = Depends(get_db),
):
    return get_alert_candidates(
        db=db,
        stock_code=stock_code,
        gpt_filter_result=gpt_filter_result,
        min_importance_score=min_importance_score,
        published_from=published_from,
        published_to=published_to,
    )


@router.get("/alerts/summary", response_model=AlertCandidateSummary)
def alerts_summary(db: Session = Depends(get_db)):
    return get_alert_summary(db)


@router.post("/alerts/send/dry-run", response_model=AlertSendResult)
def dry_run_alert_send(payload: AlertSendRequest, db: Session = Depends(get_db)):
    return dry_run_send_alerts(db, payload)


@router.post("/alerts/send", response_model=AlertSendResult)
def send_news_alerts(payload: AlertSendRequest, db: Session = Depends(get_db)):
    return send_alerts(db, payload)


@router.get("/alerts/histories", response_model=list[AlertHistoryRead])
def alert_histories(status: str | None = None, db: Session = Depends(get_db)):
    return get_alert_histories(db, status=status)


@router.get("/alerts/histories/summary", response_model=AlertHistorySummary)
def alert_histories_summary(db: Session = Depends(get_db)):
    return get_alert_histories_summary(db)


@router.get("/{news_id}/trades", response_model=list[NewsTradeRead])
def related_trades(news_id: int, db: Session = Depends(get_db)):
    return get_news_related_trades(db, news_id)


@router.get("/{news_id}", response_model=NewsRead)
def detail_item(news_id: int, db: Session = Depends(get_db)):
    return get_news_detail(db, news_id)
