from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.responses import ok
from app.db.session import get_db
from app.domains.memos.service import get_memos, get_tags

router = APIRouter()


@router.get("")
def memos(db: Session = Depends(get_db)):
    return ok(get_memos(db))


@router.get("/tags")
def tags(db: Session = Depends(get_db)):
    return ok(get_tags(db))
