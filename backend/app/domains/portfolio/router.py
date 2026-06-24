from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.responses import ok
from app.db.session import get_db
from app.domains.portfolio.service import get_fund_pools

router = APIRouter()


@router.get("/fund-pools")
def fund_pools(db: Session = Depends(get_db)):
    return ok(get_fund_pools(db))


@router.get("/summary")
def summary():
    return ok({"menu": "portfolio", "description": "자금 풀, 현금, 보유현황 요약"})
