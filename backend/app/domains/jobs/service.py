from datetime import datetime, timedelta
from typing import Any

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import ScheduledJob
from app.domains.alerts.schemas import PriceAlertEvaluationRequest
from app.domains.alerts.service import evaluate_price_alerts, evaluate_price_alerts_dry_run
from app.domains.jobs import repository
from app.domains.jobs.schemas import JobBatchRunRequest, JobRead, JobRunRequest, JobRunResult, JobSummary
from app.domains.news.schemas import AlertSendRequest, GptRunRequest, MarketNewsCollectRequest
from app.domains.news.service import (
    collect_market_news,
    dry_run_send_alerts,
    recalculate_alert_candidates,
    run_gpt_filter,
    run_gpt_summary,
    send_alerts,
)
from app.domains.prices.schemas import KrxDailyCollectRequest, KrxRangeCollectRequest
from app.domains.prices.service import collect_krx_daily_prices, collect_krx_range_prices

SUPPORTED_JOB_DEFINITIONS: dict[str, dict[str, Any]] = {
    "krx_price_daily": {
        "job_name": "KRX Daily Price Collect",
        "schedule_type": "manual",
        "config_json": {"markets": ["KOSPI", "KOSDAQ"], "dry_run": True},
    },
    "krx_price_range": {
        "job_name": "KRX Range Price Collect",
        "schedule_type": "manual",
        "config_json": {"markets": ["KOSPI", "KOSDAQ"], "dry_run": True, "skip_empty": True},
    },
    "naver_news_collect": {
        "job_name": "Naver News Collect",
        "schedule_type": "manual",
        "config_json": {"pages": 1, "max_items": 10},
    },
    "gpt_news_summary": {
        "job_name": "GPT News Summary",
        "schedule_type": "manual",
        "config_json": {"limit": 5, "dry_run": True},
    },
    "gpt_news_filter": {
        "job_name": "GPT News Filter",
        "schedule_type": "manual",
        "config_json": {"limit": 5, "dry_run": True},
    },
    "news_alert_candidate": {
        "job_name": "News Alert Candidate Recalculate",
        "schedule_type": "manual",
        "config_json": {},
    },
    "news_alert_send": {
        "job_name": "News Alert Send",
        "schedule_type": "manual",
        "config_json": {"limit": 10, "force": False, "dry_run": True},
    },
    "price_alert_evaluate": {
        "job_name": "Price Alert Evaluate",
        "schedule_type": "manual",
        "config_json": {"limit": 10, "force": False, "dry_run": True},
    },
}

LEGACY_JOB_KEY_ALIASES = {
    "krx_price_update": "krx_price_daily",
    "news_collect": "naver_news_collect",
}


def _ensure_supported_jobs(db: Session) -> None:
    changed = False
    for job_key, definition in SUPPORTED_JOB_DEFINITIONS.items():
        if repository.get_job_by_key(db, job_key) is None:
            repository.create_job(
                db,
                job_key=job_key,
                job_name=definition["job_name"],
                schedule_type=definition["schedule_type"],
                config_json=definition["config_json"],
            )
            changed = True
    if changed:
        db.commit()


def _recent_logs_by_job(db: Session) -> dict[int, dict[str, Any]]:
    latest: dict[int, dict[str, Any]] = {}
    for log in repository.list_job_logs(db):
        context = log.context_json or {}
        job_id = context.get("job_id")
        if not isinstance(job_id, int) or job_id in latest:
            continue
        latest[job_id] = {
            "status": context.get("status"),
            "message": context.get("message") or log.message,
            "started_at": context.get("started_at"),
            "finished_at": context.get("finished_at"),
            "result": context.get("result") or {},
        }
    return latest


def _normalize_job_key(job_key: str) -> str:
    return LEGACY_JOB_KEY_ALIASES.get(job_key, job_key)


def _visible_jobs(db: Session) -> list[ScheduledJob]:
    rows = repository.list_jobs(db)
    selected: dict[str, ScheduledJob] = {}
    for row in rows:
        normalized = _normalize_job_key(row.job_key)
        if normalized not in SUPPORTED_JOB_DEFINITIONS:
            continue
        existing = selected.get(normalized)
        if existing is None:
            selected[normalized] = row
            continue
        if existing.job_key != normalized and row.job_key == normalized:
            selected[normalized] = row
    return sorted(selected.values(), key=lambda item: _normalize_job_key(item.job_key))


def _serialize_job(job: ScheduledJob, latest_log: dict[str, Any] | None) -> JobRead:
    started_at = latest_log.get("started_at") if latest_log else None
    finished_at = latest_log.get("finished_at") if latest_log else None
    return JobRead(
        id=job.id,
        job_key=job.job_key,
        job_name=job.job_name,
        enabled=job.enabled,
        schedule_type=job.schedule_type,
        cron_expression=job.cron_expression,
        config_json=job.config_json,
        last_run_at=job.last_run_at,
        next_run_at=job.next_run_at,
        last_status=latest_log.get("status") if latest_log else None,
        last_message=latest_log.get("message") if latest_log else None,
        last_started_at=datetime.fromisoformat(started_at) if isinstance(started_at, str) else None,
        last_finished_at=datetime.fromisoformat(finished_at) if isinstance(finished_at, str) else None,
        created_at=job.created_at,
        updated_at=job.updated_at,
    )


def get_jobs(db: Session) -> list[JobRead]:
    _ensure_supported_jobs(db)
    latest_logs = _recent_logs_by_job(db)
    return [_serialize_job(job, latest_logs.get(job.id)) for job in _visible_jobs(db)]


def get_job_detail(db: Session, job_id: int) -> JobRead:
    _ensure_supported_jobs(db)
    job = repository.get_job(db, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="scheduled job not found")
    latest_logs = _recent_logs_by_job(db)
    return _serialize_job(job, latest_logs.get(job.id))


def _latest_price_date_text(db: Session) -> str:
    from app.db.models import StockPrice

    latest = db.query(StockPrice.date).order_by(StockPrice.date.desc()).first()
    if latest is None or latest[0] is None:
        return datetime.utcnow().strftime("%Y%m%d")
    return latest[0].strftime("%Y%m%d")


def _merge_config(job: ScheduledJob, payload: JobRunRequest | None) -> dict[str, Any]:
    config = dict(job.config_json or {})
    if payload and payload.config_json:
        config.update(payload.config_json)
    if payload and payload.dry_run is not None:
        config["dry_run"] = payload.dry_run
    return config


def _execute_job(db: Session, job: ScheduledJob, config: dict[str, Any]) -> tuple[str, dict[str, Any], str]:
    job_type = _normalize_job_key(job.job_key)

    if job_type == "krx_price_daily":
        bas_date = str(config.get("bas_date") or _latest_price_date_text(db))
        result = collect_krx_daily_prices(
            db,
            KrxDailyCollectRequest(
                bas_date=bas_date,
                markets=list(config.get("markets") or ["KOSPI", "KOSDAQ"]),
                dry_run=bool(config.get("dry_run", True)),
            ),
        )
        data = result.model_dump(mode="json")
        return ("success" if result.error_count == 0 else "failed", data, f"fetched {result.fetched_count}, inserted {result.inserted_count}, updated {result.updated_count}")

    if job_type == "krx_price_range":
        latest = _latest_price_date_text(db)
        date_to = str(config.get("date_to") or latest)
        date_from = str(config.get("date_from") or date_to)
        result = collect_krx_range_prices(
            db,
            KrxRangeCollectRequest(
                date_from=date_from,
                date_to=date_to,
                markets=list(config.get("markets") or ["KOSPI", "KOSDAQ"]),
                dry_run=bool(config.get("dry_run", True)),
                skip_empty=bool(config.get("skip_empty", True)),
            ),
        )
        data = result.model_dump(mode="json")
        return ("success" if result.error_count == 0 else "failed", data, f"dates {result.requested_date_count}, fetched {result.fetched_count}, inserted {result.inserted_count}")

    if job_type == "naver_news_collect":
        result = collect_market_news(
            db,
            MarketNewsCollectRequest(
                pages=int(config.get("pages", 1)),
                max_items=int(config.get("max_items", 10)),
            ),
        )
        data = {
            "job_id": result.id,
            "status": result.status,
            "new_count": result.new_count,
            "duplicate_count": result.duplicate_count,
            "excluded_count": result.excluded_count,
        }
        return ("success" if result.status in {"success", "partial_success"} else "failed", data, f"new {result.new_count}, duplicate {result.duplicate_count}, excluded {result.excluded_count}")

    if job_type == "gpt_news_summary":
        result = run_gpt_summary(
            db,
            GptRunRequest(
                limit=int(config.get("limit", 5)),
                dry_run=bool(config.get("dry_run", True)),
            ),
        )
        data = result.model_dump(mode="json")
        return ("success", data, f"target {result.target_count}, processed {result.processed_count}")

    if job_type == "gpt_news_filter":
        result = run_gpt_filter(
            db,
            GptRunRequest(
                limit=int(config.get("limit", 5)),
                dry_run=bool(config.get("dry_run", True)),
            ),
        )
        data = result.model_dump(mode="json")
        return ("success", data, f"target {result.target_count}, processed {result.processed_count}")

    if job_type == "news_alert_candidate":
        result = recalculate_alert_candidates(db)
        data = result.model_dump(mode="json")
        return ("success", data, f"processed {result.processed_count}, changed {result.changed_count}")

    if job_type == "news_alert_send":
        request = AlertSendRequest(
            limit=int(config.get("limit", 10)),
            force=bool(config.get("force", False)),
        )
        if bool(config.get("dry_run", True)):
            result = dry_run_send_alerts(db, request)
        else:
            result = send_alerts(db, request)
        data = result.model_dump(mode="json")
        return ("success", data, f"sendable {result.sendable_count}, sent {result.sent_count}, skipped {result.skipped_count}")

    if job_type == "price_alert_evaluate":
        request = PriceAlertEvaluationRequest(
            alert_ids=config.get("alert_ids"),
            limit=int(config.get("limit", 10)),
            force=bool(config.get("force", False)),
        )
        if bool(config.get("dry_run", True)):
            result = evaluate_price_alerts_dry_run(db, request)
        else:
            result = evaluate_price_alerts(db, request)
        data = result.model_dump(mode="json")
        return ("success", data, f"evaluated {result.evaluated_count}, sent {result.sent_count}, skipped {result.skipped_count}")

    raise HTTPException(status_code=400, detail=f"unsupported job_key: {job.job_key}")


def run_job(db: Session, job_id: int, payload: JobRunRequest | None = None) -> JobRunResult:
    _ensure_supported_jobs(db)
    job = repository.get_job(db, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="scheduled job not found")
    started_at = datetime.utcnow()
    status = "failed"
    message = ""
    result: dict[str, Any] = {}
    try:
        config = _merge_config(job, payload)
        status, result, message = _execute_job(db, job, config)
    except Exception as exc:  # noqa: BLE001
        db.rollback()
        status = "failed"
        message = str(exc)
        result = {}
    finished_at = datetime.utcnow()
    repository.update_job_run_timestamp(db, job, finished_at)
    repository.create_job_log(
        db,
        level="info" if status == "success" else "error",
        message=message or status,
        context={
            "job_id": job.id,
            "job_key": job.job_key,
            "status": status,
            "started_at": started_at.isoformat(),
            "finished_at": finished_at.isoformat(),
            "message": message,
            "result": result,
        },
    )
    db.commit()
    return JobRunResult(
        job_id=job.id,
        job_key=job.job_key,
        status=status,
        started_at=started_at,
        finished_at=finished_at,
        message=message,
        result=result,
    )


def run_jobs(db: Session, payload: JobBatchRunRequest) -> list[JobRunResult]:
    _ensure_supported_jobs(db)
    jobs = _visible_jobs(db)
    selected = [job for job in jobs if job.enabled] if not payload.job_ids else [job for job in jobs if job.id in set(payload.job_ids)]
    results: list[JobRunResult] = []
    for job in selected:
        results.append(run_job(db, job.id, JobRunRequest(dry_run=payload.dry_run, config_json=payload.config_json)))
    return results


def get_job_summary(db: Session) -> JobSummary:
    jobs = get_jobs(db)
    success_count = sum(1 for job in jobs if job.last_status == "success")
    failed_count = sum(1 for job in jobs if job.last_status == "failed")
    never_run_count = sum(1 for job in jobs if job.last_run_at is None)
    recent_runs: list[JobRunResult] = []
    for log in repository.list_job_logs(db, limit=10):
        context = log.context_json or {}
        job_id = context.get("job_id")
        job_key = context.get("job_key")
        started_at = context.get("started_at")
        finished_at = context.get("finished_at")
        if not isinstance(job_id, int) or not isinstance(job_key, str) or not isinstance(started_at, str) or not isinstance(finished_at, str):
            continue
        recent_runs.append(
            JobRunResult(
                job_id=job_id,
                job_key=job_key,
                status=str(context.get("status") or "failed"),
                started_at=datetime.fromisoformat(started_at),
                finished_at=datetime.fromisoformat(finished_at),
                message=str(context.get("message") or log.message),
                result=context.get("result") or {},
            )
        )
    return JobSummary(
        total_count=len(jobs),
        enabled_count=sum(1 for job in jobs if job.enabled),
        disabled_count=sum(1 for job in jobs if not job.enabled),
        success_count=success_count,
        failed_count=failed_count,
        never_run_count=never_run_count,
        recent_runs=recent_runs,
    )
