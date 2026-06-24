from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.common.responses import ok
from app.db.session import get_db
from app.domains.collection.schemas import (
    CollectionRuleCreate,
    CollectionRuleRead,
    CollectionRuleUpdate,
    CollectionStockRead,
    CollectionStockSummary,
    CollectionStockUpdate,
    ImportResult,
    IndexConstituentImportRequest,
    IndexConstituentRead,
    RecalculateResult,
)
from app.domains.collection.service import (
    create_collection_rule,
    delete_collection_rule,
    exclude_collection_stock,
    get_collection_rules,
    get_collection_stocks,
    get_collection_stocks_summary,
    get_index_constituents,
    get_index_constituents_summary,
    import_index_constituents,
    include_collection_stock,
    recalculate_collection_stocks,
    update_collection_rule,
    update_collection_stock,
)

router = APIRouter()


@router.post("/index-constituents/import", response_model=ImportResult)
def import_index_constituents_item(payload: IndexConstituentImportRequest, db: Session = Depends(get_db)):
    return import_index_constituents(db, payload)


@router.get("/index-constituents", response_model=list[IndexConstituentRead])
def list_index_constituents(index_code: str | None = None, db: Session = Depends(get_db)):
    return get_index_constituents(db, index_code=index_code)


@router.get("/index-constituents/summary")
def index_constituents_summary(db: Session = Depends(get_db)):
    return ok(get_index_constituents_summary(db))


@router.get("/stocks", response_model=list[CollectionStockRead])
def list_collection_stocks(
    collect_enabled: bool | None = None,
    collect_news: bool | None = None,
    collect_alert_enabled: bool | None = None,
    priority: str | None = None,
    collect_reason: str | None = None,
    market: str | None = None,
    index_code: str | None = None,
    is_favorite: bool | None = None,
    keyword: str | None = None,
    db: Session = Depends(get_db),
):
    return get_collection_stocks(
        db,
        collect_enabled=collect_enabled,
        collect_news=collect_news,
        collect_alert_enabled=collect_alert_enabled,
        priority=priority,
        collect_reason=collect_reason,
        market=market,
        index_code=index_code,
        is_favorite=is_favorite,
        keyword=keyword,
    )


@router.get("/stocks/summary", response_model=CollectionStockSummary)
def collection_stocks_summary(db: Session = Depends(get_db)):
    return get_collection_stocks_summary(db)


@router.post("/stocks/recalculate", response_model=RecalculateResult)
def recalculate_collection_stock_items(db: Session = Depends(get_db)):
    return recalculate_collection_stocks(db)


@router.patch("/stocks/{stock_id}", response_model=CollectionStockRead)
def update_collection_stock_item(stock_id: int, payload: CollectionStockUpdate, db: Session = Depends(get_db)):
    return update_collection_stock(db, stock_id, payload)


@router.post("/stocks/{stock_id}/include", response_model=CollectionStockRead)
def include_collection_stock_item(stock_id: int, db: Session = Depends(get_db)):
    return include_collection_stock(db, stock_id)


@router.post("/stocks/{stock_id}/exclude", response_model=CollectionStockRead)
def exclude_collection_stock_item(stock_id: int, db: Session = Depends(get_db)):
    return exclude_collection_stock(db, stock_id)


@router.get("/rules", response_model=list[CollectionRuleRead])
def rules(db: Session = Depends(get_db)):
    return get_collection_rules(db)


@router.post("/rules", response_model=CollectionRuleRead, status_code=201)
def create_rule(payload: CollectionRuleCreate, db: Session = Depends(get_db)):
    return create_collection_rule(db, payload)


@router.patch("/rules/{rule_id}", response_model=CollectionRuleRead)
def update_rule(rule_id: int, payload: CollectionRuleUpdate, db: Session = Depends(get_db)):
    return update_collection_rule(db, rule_id, payload)


@router.delete("/rules/{rule_id}", status_code=204)
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    delete_collection_rule(db, rule_id)
    return Response(status_code=204)


@router.get("/summary")
def summary():
    return ok({"menu": "collection", "description": "수집 종목 조건 및 최종 대상 관리"})
