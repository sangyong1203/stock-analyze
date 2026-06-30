from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.domains.portfolio.schemas import PortfolioSummary
from app.domains.portfolio.service import get_portfolio_summary

router = APIRouter()


@router.get("/summary", response_model=PortfolioSummary)
def summary(db: Session = Depends(get_db)):
    return get_portfolio_summary(db)
