from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.domains.alerts.schemas import (
    AlertHistoryRead,
    PriceAlertCreate,
    PriceAlertEvaluationRequest,
    PriceAlertEvaluationResult,
    PriceAlertRead,
    PriceAlertSummary,
    PriceAlertUpdate,
)
from app.domains.alerts.service import (
    create_price_alert,
    delete_price_alert,
    evaluate_price_alerts,
    evaluate_price_alerts_dry_run,
    get_price_alert_detail,
    get_price_alert_histories,
    get_price_alert_summary,
    get_price_alerts,
    update_price_alert,
)

router = APIRouter()


@router.get("", response_model=list[PriceAlertRead])
def list_items(
    stock_id: int | None = None,
    enabled: bool | None = None,
    db: Session = Depends(get_db),
):
    return get_price_alerts(db, stock_id=stock_id, enabled=enabled)


@router.post("", response_model=PriceAlertRead, status_code=201)
def create_item(payload: PriceAlertCreate, db: Session = Depends(get_db)):
    return create_price_alert(db, payload)


@router.get("/summary", response_model=PriceAlertSummary)
def summary(db: Session = Depends(get_db)):
    return get_price_alert_summary(db)


@router.post("/evaluate/dry-run", response_model=PriceAlertEvaluationResult)
def evaluate_dry_run(payload: PriceAlertEvaluationRequest, db: Session = Depends(get_db)):
    return evaluate_price_alerts_dry_run(db, payload)


@router.post("/evaluate", response_model=PriceAlertEvaluationResult)
def evaluate(payload: PriceAlertEvaluationRequest, db: Session = Depends(get_db)):
    return evaluate_price_alerts(db, payload)


@router.get("/histories", response_model=list[AlertHistoryRead])
def histories(status: str | None = None, db: Session = Depends(get_db)):
    return get_price_alert_histories(db, status=status)


@router.get("/{alert_id}", response_model=PriceAlertRead)
def detail_item(alert_id: int, db: Session = Depends(get_db)):
    return get_price_alert_detail(db, alert_id)


@router.patch("/{alert_id}", response_model=PriceAlertRead)
def update_item(alert_id: int, payload: PriceAlertUpdate, db: Session = Depends(get_db)):
    return update_price_alert(db, alert_id, payload)


@router.delete("/{alert_id}", status_code=204)
def delete_item(alert_id: int, db: Session = Depends(get_db)):
    delete_price_alert(db, alert_id)
    return Response(status_code=204)
