from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.responses import ok
from app.db.session import get_db
from app.domains.alerts.service import get_price_alerts

router = APIRouter()


@router.get("/price")
def price_alerts(db: Session = Depends(get_db)):
    return ok(get_price_alerts(db))


@router.get("/summary")
def summary():
    return ok({"menu": "alerts", "description": "가격 알림, 뉴스 알림, 발송 이력 관리"})
