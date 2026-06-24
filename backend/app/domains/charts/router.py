from fastapi import APIRouter

from app.common.responses import ok
from app.domains.charts.service import get_chart_summary

router = APIRouter()


@router.get("/summary")
def summary():
    return ok(get_chart_summary())
