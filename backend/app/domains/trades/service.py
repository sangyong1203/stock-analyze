from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import FundPool, FundTransaction, News, Stock, Trade, TradeNewsLink
from app.domains.holdings.service import recalculate_holdings
from app.domains.trades import repository
from app.domains.trades.schemas import NewsTradeRead, TradeCreate, TradeNewsLinkCreate, TradeNewsRead, TradeRead, TradeUpdate


def _to_decimal(value: Decimal | int | float | str | None) -> Decimal:
    if value is None:
        return Decimal("0")
    return value if isinstance(value, Decimal) else Decimal(str(value))


def _normalize_trade_type(value: str) -> str:
    normalized = value.lower()
    if normalized not in {"buy", "sell"}:
        raise HTTPException(status_code=400, detail="trade_type must be buy or sell")
    return normalized


def _serialize_trade(item: Trade, fund_pool_name: str, stock_code: str, stock_name: str) -> TradeRead:
    return TradeRead(
        id=item.id,
        fund_pool_id=item.fund_pool_id,
        fund_pool_name=fund_pool_name,
        stock_id=item.stock_id,
        stock_code=stock_code,
        stock_name=stock_name,
        trade_type=item.trade_type,
        trade_date=item.trade_date,
        quantity=item.quantity,
        price=item.price,
        amount=item.amount,
        fee=item.fee,
        tax=item.tax,
        total_amount=item.total_amount,
        average_price_at_trade=item.average_price_at_trade,
        realized_profit_loss=item.realized_profit_loss,
        realized_profit_loss_rate=item.realized_profit_loss_rate,
        reason=item.reason,
        memo=item.memo,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )


def _get_fund_pool(db: Session, fund_pool_id: int) -> FundPool:
    item = db.get(FundPool, fund_pool_id)
    if item is None:
        raise HTTPException(status_code=404, detail="fund pool not found")
    return item


def _get_stock(db: Session, stock_id: int) -> Stock:
    item = db.get(Stock, stock_id)
    if item is None:
        raise HTTPException(status_code=404, detail="stock not found")
    return item


def _get_news(db: Session, news_id: int) -> News:
    item = db.get(News, news_id)
    if item is None:
        raise HTTPException(status_code=404, detail="news not found")
    return item


def _serialize_trade_news_link(item: TradeNewsLink, title: str, source: str | None, published_at) -> TradeNewsRead:
    return TradeNewsRead(
        id=item.id,
        trade_id=item.trade_id,
        news_id=item.news_id,
        link_type=item.link_type,
        memo=item.memo,
        created_at=item.created_at,
        title=title,
        source=source,
        published_at=published_at,
    )


def _serialize_news_trade_link(row) -> NewsTradeRead:
    item, fund_pool_name, stock_code, stock_name, fund_pool_id, stock_id, trade_type, trade_date, quantity, price = row
    return NewsTradeRead(
        id=item.id,
        trade_id=item.trade_id,
        news_id=item.news_id,
        link_type=item.link_type,
        memo=item.memo,
        created_at=item.created_at,
        fund_pool_id=fund_pool_id,
        fund_pool_name=fund_pool_name,
        stock_id=stock_id,
        stock_code=stock_code,
        stock_name=stock_name,
        trade_type=trade_type,
        trade_date=trade_date,
        quantity=quantity,
        price=price,
    )


def _build_trade_values(
    trade_type: str,
    quantity: int,
    price: Decimal,
    fee: Decimal,
    tax: Decimal,
    average_price: Decimal = Decimal("0"),
) -> dict[str, Decimal | None]:
    amount = price * Decimal(quantity)
    if trade_type == "buy":
        total_amount = amount + fee + tax
        return {
            "amount": amount,
            "total_amount": total_amount,
            "average_price_at_trade": None,
            "realized_profit_loss": None,
            "realized_profit_loss_rate": None,
        }
    sell_net_amount = amount - fee - tax
    realized_profit_loss = sell_net_amount - (average_price * Decimal(quantity))
    realized_profit_loss_rate = (realized_profit_loss / (average_price * Decimal(quantity))) if average_price > 0 else None
    return {
        "amount": amount,
        "total_amount": sell_net_amount,
        "average_price_at_trade": average_price,
        "realized_profit_loss": realized_profit_loss,
        "realized_profit_loss_rate": realized_profit_loss_rate,
    }


def _get_open_holding_average_price(db: Session, fund_pool_id: int, stock_id: int, exclude_trade_id: int | None = None) -> Decimal:
    from app.db.models import Holding, Trade as TradeModel

    if exclude_trade_id is None:
        holding = db.query(Holding).filter(Holding.fund_pool_id == fund_pool_id, Holding.stock_id == stock_id, Holding.is_closed.is_(False)).first()
        return _to_decimal(holding.average_price) if holding else Decimal("0")

    trades = (
        db.query(TradeModel)
        .filter(TradeModel.fund_pool_id == fund_pool_id, TradeModel.stock_id == stock_id, TradeModel.id != exclude_trade_id)
        .order_by(TradeModel.trade_date.asc(), TradeModel.id.asc())
        .all()
    )
    quantity = 0
    cost_basis = Decimal("0")
    for trade in trades:
        if trade.trade_type.lower() == "buy":
            quantity += trade.quantity
            cost_basis += _to_decimal(trade.total_amount)
        else:
            average_price = cost_basis / Decimal(quantity) if quantity > 0 else Decimal("0")
            quantity = max(0, quantity - trade.quantity)
            cost_basis = max(Decimal("0"), cost_basis - (average_price * Decimal(trade.quantity)))
    return (cost_basis / Decimal(quantity)) if quantity > 0 else Decimal("0")


def _validate_sell_quantity(db: Session, fund_pool_id: int, stock_id: int, quantity: int, exclude_trade_id: int | None = None) -> None:
    from app.db.models import Trade as TradeModel

    trades = db.query(TradeModel).filter(TradeModel.fund_pool_id == fund_pool_id, TradeModel.stock_id == stock_id)
    if exclude_trade_id is not None:
        trades = trades.filter(TradeModel.id != exclude_trade_id)
    current_quantity = 0
    for trade in trades.order_by(TradeModel.trade_date.asc(), TradeModel.id.asc()).all():
        current_quantity += trade.quantity if trade.trade_type.lower() == "buy" else -trade.quantity
    if current_quantity < quantity:
        raise HTTPException(status_code=400, detail="sell quantity exceeds current holding quantity")


def _apply_trade_fund_effect(fund_pool: FundPool, trade_type: str, total_amount: Decimal) -> None:
    if trade_type == "buy":
        if fund_pool.cash_balance < total_amount:
            raise HTTPException(status_code=400, detail="insufficient cash balance")
        fund_pool.cash_balance -= total_amount
        return
    fund_pool.cash_balance += total_amount


def _sync_trade_fund_transaction(db: Session, trade: Trade) -> None:
    item = repository.get_trade_fund_transaction(db, trade.id)
    if item is None:
        item = FundTransaction(
            fund_pool_id=trade.fund_pool_id,
            transaction_type=trade.trade_type,
            amount=trade.total_amount,
            currency="KRW",
            related_trade_id=trade.id,
            memo=trade.memo,
            transaction_date=trade.trade_date,
        )
        db.add(item)
        return
    item.fund_pool_id = trade.fund_pool_id
    item.transaction_type = trade.trade_type
    item.amount = trade.total_amount
    item.memo = trade.memo
    item.transaction_date = trade.trade_date


def get_trade_list(db: Session):
    return [_serialize_trade(item, fund_pool_name, stock_code, stock_name) for item, fund_pool_name, stock_code, stock_name in repository.list_trades(db)]


def get_trade_detail(db: Session, trade_id: int) -> TradeRead:
    row = repository.get_trade_detail_row(db, trade_id)
    if row is None:
        raise HTTPException(status_code=404, detail="trade not found")
    item, fund_pool_name, stock_code, stock_name = row
    return _serialize_trade(item, fund_pool_name, stock_code, stock_name)


def create_trade(db: Session, payload: TradeCreate) -> TradeRead:
    trade_type = _normalize_trade_type(payload.trade_type)
    fund_pool = _get_fund_pool(db, payload.fund_pool_id)
    _get_stock(db, payload.stock_id)
    price = _to_decimal(payload.price)
    fee = _to_decimal(payload.fee)
    tax = _to_decimal(payload.tax)
    if trade_type == "sell":
        _validate_sell_quantity(db, payload.fund_pool_id, payload.stock_id, payload.quantity)
    average_price = _get_open_holding_average_price(db, payload.fund_pool_id, payload.stock_id) if trade_type == "sell" else Decimal("0")
    values = _build_trade_values(trade_type, payload.quantity, price, fee, tax, average_price)
    item = Trade(
        fund_pool_id=payload.fund_pool_id,
        stock_id=payload.stock_id,
        trade_type=trade_type,
        trade_date=payload.trade_date,
        quantity=payload.quantity,
        price=price,
        amount=values["amount"],
        fee=fee,
        tax=tax,
        total_amount=values["total_amount"],
        average_price_at_trade=values["average_price_at_trade"],
        realized_profit_loss=values["realized_profit_loss"],
        realized_profit_loss_rate=values["realized_profit_loss_rate"],
        reason=payload.reason,
        memo=payload.memo,
    )
    _apply_trade_fund_effect(fund_pool, trade_type, _to_decimal(values["total_amount"]))
    db.add(item)
    db.flush()
    _sync_trade_fund_transaction(db, item)
    db.commit()
    recalculate_holdings(db, payload.fund_pool_id)
    return get_trade_detail(db, item.id)


def update_trade(db: Session, trade_id: int, payload: TradeUpdate) -> TradeRead:
    item = repository.get_trade(db, trade_id)
    if item is None:
        raise HTTPException(status_code=404, detail="trade not found")

    original_pool_id = item.fund_pool_id
    original_total_amount = _to_decimal(item.total_amount)
    original_trade_type = item.trade_type.lower()
    original_pool = _get_fund_pool(db, original_pool_id)

    updated = payload.model_dump(exclude_unset=True)
    target_fund_pool_id = updated.get("fund_pool_id", item.fund_pool_id)
    target_stock_id = updated.get("stock_id", item.stock_id)
    target_trade_type = _normalize_trade_type(updated.get("trade_type", item.trade_type))
    target_quantity = updated.get("quantity", item.quantity)
    target_price = _to_decimal(updated.get("price", item.price))
    target_fee = _to_decimal(updated.get("fee", item.fee))
    target_tax = _to_decimal(updated.get("tax", item.tax))

    _get_fund_pool(db, target_fund_pool_id)
    _get_stock(db, target_stock_id)
    if target_trade_type == "sell":
        _validate_sell_quantity(db, target_fund_pool_id, target_stock_id, target_quantity, exclude_trade_id=trade_id)
    average_price = _get_open_holding_average_price(db, target_fund_pool_id, target_stock_id, exclude_trade_id=trade_id) if target_trade_type == "sell" else Decimal("0")
    recalculated = _build_trade_values(target_trade_type, target_quantity, target_price, target_fee, target_tax, average_price)

    if original_trade_type == "buy":
        original_pool.cash_balance += original_total_amount
    else:
        original_pool.cash_balance -= original_total_amount

    target_pool = _get_fund_pool(db, target_fund_pool_id)
    _apply_trade_fund_effect(target_pool, target_trade_type, _to_decimal(recalculated["total_amount"]))

    item.fund_pool_id = target_fund_pool_id
    item.stock_id = target_stock_id
    item.trade_type = target_trade_type
    item.trade_date = updated.get("trade_date", item.trade_date)
    item.quantity = target_quantity
    item.price = target_price
    item.amount = recalculated["amount"]
    item.fee = target_fee
    item.tax = target_tax
    item.total_amount = recalculated["total_amount"]
    item.average_price_at_trade = recalculated["average_price_at_trade"]
    item.realized_profit_loss = recalculated["realized_profit_loss"]
    item.realized_profit_loss_rate = recalculated["realized_profit_loss_rate"]
    item.reason = updated.get("reason", item.reason)
    item.memo = updated.get("memo", item.memo)
    _sync_trade_fund_transaction(db, item)
    db.commit()
    recalculate_holdings(db, original_pool_id)
    if target_fund_pool_id != original_pool_id:
        recalculate_holdings(db, target_fund_pool_id)
    return get_trade_detail(db, item.id)


def delete_trade(db: Session, trade_id: int) -> dict[str, int]:
    item = repository.get_trade(db, trade_id)
    if item is None:
        raise HTTPException(status_code=404, detail="trade not found")

    fund_pool_id = item.fund_pool_id
    fund_pool = _get_fund_pool(db, fund_pool_id)
    total_amount = _to_decimal(item.total_amount)
    if item.trade_type.lower() == "buy":
        fund_pool.cash_balance += total_amount
    else:
        if fund_pool.cash_balance < total_amount:
            raise HTTPException(status_code=400, detail="cannot delete sell trade because fund cash balance is lower than the sell proceeds already applied")
        fund_pool.cash_balance -= total_amount

    related_tx = repository.get_trade_fund_transaction(db, trade_id)
    if related_tx is not None:
        db.delete(related_tx)
    db.delete(item)
    db.commit()
    recalculate_holdings(db, fund_pool_id)
    return {"deleted_trade_id": trade_id}


def get_trade_related_news(db: Session, trade_id: int):
    if repository.get_trade(db, trade_id) is None:
        raise HTTPException(status_code=404, detail="trade not found")
    return [_serialize_trade_news_link(item, title, source, published_at) for item, title, source, published_at in repository.list_trade_news_links(db, trade_id)]


def link_trade_news(db: Session, trade_id: int, payload: TradeNewsLinkCreate):
    if repository.get_trade(db, trade_id) is None:
        raise HTTPException(status_code=404, detail="trade not found")
    _get_news(db, payload.news_id)
    if repository.get_trade_news_link(db, trade_id, payload.news_id) is not None:
        raise HTTPException(status_code=409, detail="trade news link already exists")
    item = TradeNewsLink(
        trade_id=trade_id,
        news_id=payload.news_id,
        link_type=payload.link_type.strip(),
        memo=payload.memo,
    )
    db.add(item)
    db.commit()
    return get_trade_related_news(db, trade_id)[0]


def unlink_trade_news(db: Session, trade_id: int, news_id: int) -> dict[str, int]:
    item = repository.get_trade_news_link(db, trade_id, news_id)
    if item is None:
        raise HTTPException(status_code=404, detail="trade news link not found")
    db.delete(item)
    db.commit()
    return {"trade_id": trade_id, "news_id": news_id}


def get_news_related_trades(db: Session, news_id: int):
    _get_news(db, news_id)
    return [_serialize_news_trade_link(row) for row in repository.list_news_trade_links(db, news_id)]
