from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.domains.funds.schemas import FundPoolCreate, FundPoolRead, FundsSummary, FundTransactionCreate, FundTransactionRead
from app.domains.funds.service import create_pool, create_transaction, get_summary, list_pools, list_transactions

router = APIRouter()


@router.get("/pools", response_model=list[FundPoolRead])
def fund_pools(db: Session = Depends(get_db)):
    return list_pools(db)


@router.post("/pools", response_model=FundPoolRead, status_code=201)
def create_fund_pool(payload: FundPoolCreate, db: Session = Depends(get_db)):
    return create_pool(db, payload)


@router.get("/transactions", response_model=list[FundTransactionRead])
def fund_transactions(fund_pool_id: int | None = None, db: Session = Depends(get_db)):
    return list_transactions(db, fund_pool_id)


@router.post("/transactions", response_model=FundTransactionRead, status_code=201)
def create_fund_transaction(payload: FundTransactionCreate, db: Session = Depends(get_db)):
    return create_transaction(db, payload)


@router.get("/summary", response_model=FundsSummary)
def funds_summary(db: Session = Depends(get_db)):
    return get_summary(db)
