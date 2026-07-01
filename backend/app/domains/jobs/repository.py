from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models import ScheduledJob, SystemLog


def list_jobs(db: Session):
    return db.query(ScheduledJob).order_by(ScheduledJob.job_key.asc()).all()


def get_job(db: Session, job_id: int):
    return db.get(ScheduledJob, job_id)


def get_job_by_key(db: Session, job_key: str):
    return db.query(ScheduledJob).filter(ScheduledJob.job_key == job_key).first()


def create_job(
    db: Session,
    *,
    job_key: str,
    job_name: str,
    schedule_type: str,
    config_json: dict | None,
    enabled: bool = True,
    cron_expression: str | None = None,
):
    item = ScheduledJob(
        job_key=job_key,
        job_name=job_name,
        enabled=enabled,
        schedule_type=schedule_type,
        cron_expression=cron_expression,
        config_json=config_json,
    )
    db.add(item)
    db.flush()
    return item


def update_job_run_timestamp(db: Session, job: ScheduledJob, finished_at: datetime) -> None:
    job.last_run_at = finished_at
    job.updated_at = finished_at


def create_job_log(
    db: Session,
    *,
    level: str,
    message: str,
    context: dict,
):
    db.add(
        SystemLog(
            level=level,
            category="job_runner",
            message=message,
            context_json=context,
            created_at=datetime.utcnow(),
        )
    )


def list_job_logs(db: Session, limit: int = 200):
    return (
        db.query(SystemLog)
        .filter(SystemLog.category == "job_runner")
        .order_by(SystemLog.created_at.desc(), SystemLog.id.desc())
        .limit(limit)
        .all()
    )

