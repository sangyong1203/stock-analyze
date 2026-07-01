from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.domains.jobs.schemas import JobBatchRunRequest, JobRead, JobRunRequest, JobRunResult, JobSummary
from app.domains.jobs.service import get_job_detail, get_jobs, get_job_summary, run_job, run_jobs

router = APIRouter()


@router.get("", response_model=list[JobRead])
def list_items(db: Session = Depends(get_db)):
    return get_jobs(db)


@router.get("/summary", response_model=JobSummary)
def summary(db: Session = Depends(get_db)):
    return get_job_summary(db)


@router.get("/{job_id}", response_model=JobRead)
def detail_item(job_id: int, db: Session = Depends(get_db)):
    return get_job_detail(db, job_id)


@router.post("/run", response_model=list[JobRunResult])
def run_items(payload: JobBatchRunRequest, db: Session = Depends(get_db)):
    return run_jobs(db, payload)


@router.post("/{job_id}/run", response_model=JobRunResult)
def run_item(job_id: int, payload: JobRunRequest, db: Session = Depends(get_db)):
    return run_job(db, job_id, payload)
