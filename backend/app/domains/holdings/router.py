from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.domains.holdings.schemas import HoldingRead, HoldingRecalculateResult, HoldingSummary
from app.domains.holdings.service import get_holding_list, get_holding_summary, recalculate_holdings

router = APIRouter()


@router.get("", response_model=list[HoldingRead])
def holdings(db: Session = Depends(get_db)):
    return get_holding_list(db)


@router.get("/summary", response_model=HoldingSummary)
def holdings_summary(db: Session = Depends(get_db)):
    return get_holding_summary(db)


@router.post("/recalculate", response_model=HoldingRecalculateResult)
def recalculate(fund_pool_id: int | None = None, db: Session = Depends(get_db)):
    return recalculate_holdings(db, fund_pool_id)
