from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.responses import ok
from app.db.session import get_db
from app.domains.trades.service import get_trade_list

router = APIRouter()


@router.get("")
def list_items(db: Session = Depends(get_db)):
    return ok(get_trade_list(db))


@router.get("/summary")
def summary():
    return ok({"menu": "trades", "description": "매수/매도 기록과 관련 뉴스 연결"})
