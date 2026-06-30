from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.db.models import Holding, Stock, Trade
from app.domains.holdings import repository
from app.domains.holdings.schemas import HoldingRead, HoldingRecalculateResult, HoldingSummary


@dataclass
class _HoldingAccumulator:
    stock_id: int
    quantity: int = 0
    cost_basis: Decimal = Decimal("0")
    realized_profit_loss: Decimal = Decimal("0")
    first_buy_date: date | None = None
    last_trade_date: date | None = None


def _to_decimal(value: Decimal | int | float | str | None) -> Decimal:
    if value is None:
        return Decimal("0")
    return value if isinstance(value, Decimal) else Decimal(str(value))


def _safe_ratio(numerator: Decimal, denominator: Decimal) -> Decimal | None:
    if denominator == 0:
        return None
    return numerator / denominator


def _serialize_holding(item: Holding, fund_pool_name: str, stock_code: str, stock_name: str) -> HoldingRead:
    return HoldingRead(
        id=item.id,
        fund_pool_id=item.fund_pool_id,
        fund_pool_name=fund_pool_name,
        stock_id=item.stock_id,
        stock_code=stock_code,
        stock_name=stock_name,
        quantity=item.quantity,
        average_price=item.average_price,
        total_buy_amount=item.total_buy_amount,
        current_price=item.current_price,
        market_value=item.market_value,
        unrealized_profit_loss=item.unrealized_profit_loss,
        unrealized_profit_loss_rate=item.unrealized_profit_loss_rate,
        realized_profit_loss=item.realized_profit_loss,
        first_buy_date=item.first_buy_date,
        last_trade_date=item.last_trade_date,
        is_closed=item.is_closed,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )


def recalculate_holdings(db: Session, fund_pool_id: int | None = None) -> HoldingRecalculateResult:
    target_pool_ids = repository.list_target_pool_ids(db, fund_pool_id)
    processed_trade_count = 0

    for pool_id in target_pool_ids:
        trades = (
            db.query(Trade)
            .filter(Trade.fund_pool_id == pool_id)
            .order_by(Trade.trade_date.asc(), Trade.id.asc())
            .all()
        )
        processed_trade_count += len(trades)
        accumulators: dict[int, _HoldingAccumulator] = {}

        for trade in trades:
            trade_type = trade.trade_type.lower()
            amount = _to_decimal(trade.amount)
            fee = _to_decimal(trade.fee)
            tax = _to_decimal(trade.tax)
            total_amount = _to_decimal(trade.total_amount)

            item = accumulators.setdefault(trade.stock_id, _HoldingAccumulator(stock_id=trade.stock_id))
            item.last_trade_date = trade.trade_date

            if trade_type == "buy":
                item.quantity += trade.quantity
                item.cost_basis += total_amount
                if item.first_buy_date is None:
                    item.first_buy_date = trade.trade_date
                continue

            if trade_type == "sell":
                if item.quantity <= 0:
                    item.realized_profit_loss += amount - fee - tax
                    item.quantity = 0
                    item.cost_basis = Decimal("0")
                    continue
                average_price = item.cost_basis / Decimal(item.quantity) if item.quantity else Decimal("0")
                sell_net_amount = amount - fee - tax
                realized_profit_loss = sell_net_amount - (average_price * Decimal(trade.quantity))
                item.realized_profit_loss += realized_profit_loss
                item.quantity = max(0, item.quantity - trade.quantity)
                item.cost_basis = max(Decimal("0"), item.cost_basis - (average_price * Decimal(trade.quantity)))

        db.query(Holding).filter(Holding.fund_pool_id == pool_id).delete(synchronize_session=False)

        if not accumulators:
            continue

        stocks = {
            stock.id: stock
            for stock in db.query(Stock).filter(Stock.id.in_(list(accumulators.keys()))).all()
        }
        for stock_id, item in accumulators.items():
            stock = stocks.get(stock_id)
            quantity_decimal = Decimal(item.quantity)
            average_price = (item.cost_basis / quantity_decimal) if item.quantity > 0 else Decimal("0")
            current_price = _to_decimal(stock.current_price) if stock and stock.current_price is not None else None
            market_value = (current_price * quantity_decimal) if current_price is not None and item.quantity > 0 else None
            unrealized_profit_loss = (market_value - item.cost_basis) if market_value is not None else None
            unrealized_profit_loss_rate = _safe_ratio(unrealized_profit_loss, item.cost_basis) if unrealized_profit_loss is not None else None
            db.add(
                Holding(
                    fund_pool_id=pool_id,
                    stock_id=stock_id,
                    quantity=item.quantity,
                    average_price=average_price,
                    total_buy_amount=item.cost_basis,
                    current_price=current_price,
                    market_value=market_value,
                    unrealized_profit_loss=unrealized_profit_loss,
                    unrealized_profit_loss_rate=unrealized_profit_loss_rate,
                    realized_profit_loss=item.realized_profit_loss,
                    first_buy_date=item.first_buy_date,
                    last_trade_date=item.last_trade_date,
                    is_closed=item.quantity <= 0,
                )
            )

    db.commit()
    holding_count, _closed_count, _market_value, _upl, _realized = repository.get_holding_summary_values(db)
    return HoldingRecalculateResult(fund_pool_ids=target_pool_ids, processed_trade_count=processed_trade_count, holding_count=holding_count)


def get_holding_list(db: Session) -> list[HoldingRead]:
    return [_serialize_holding(item, fund_pool_name, stock_code, stock_name) for item, fund_pool_name, stock_code, stock_name, _market in repository.list_holdings(db)]


def get_holding_summary(db: Session) -> HoldingSummary:
    holding_count, closed_holding_count, total_market_value, total_unrealized_profit_loss, total_realized_profit_loss = repository.get_holding_summary_values(db)
    return HoldingSummary(
        holding_count=holding_count,
        closed_holding_count=closed_holding_count,
        total_market_value=total_market_value,
        total_unrealized_profit_loss=total_unrealized_profit_loss,
        total_realized_profit_loss=total_realized_profit_loss,
    )
