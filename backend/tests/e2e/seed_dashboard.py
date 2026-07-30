from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.db.models import (  # noqa: E402
    AlertHistory,
    FundPool,
    Holding,
    Memo,
    News,
    PriceAlert,
    ScheduledJob,
    Stock,
    StockCollectionSetting,
    SystemLog,
    Tag,
    TagLink,
    Trade,
)
from app.db.session import SessionLocal  # noqa: E402


NOW = datetime(2026, 7, 14, 9, 0, 0)


STOCK_FIXTURES = [
    {
        "code": "005930",
        "name": "삼성전자",
        "market": "KOSPI",
        "sector": "반도체",
        "market_cap": "400000000000000",
        "current_price": "80000",
        "change_rate": "2.5",
        "quantity": 10,
        "average_price": "70000",
        "market_value": "800000",
        "profit_loss": "100000",
        "profit_rate": "0.142857",
    },
    {
        "code": "000660",
        "name": "SK하이닉스",
        "market": "KOSPI",
        "sector": "반도체",
        "market_cap": "130000000000000",
        "current_price": "180000",
        "change_rate": "-1.0",
        "quantity": 5,
        "average_price": "200000",
        "market_value": "900000",
        "profit_loss": "-100000",
        "profit_rate": "-0.1",
    },
    {
        "code": "035420",
        "name": "NAVER",
        "market": "KOSPI",
        "sector": "인터넷",
        "market_cap": "35000000000000",
        "current_price": "210000",
        "change_rate": "1.2",
        "quantity": 2,
        "average_price": "200000",
        "market_value": "420000",
        "profit_loss": "20000",
        "profit_rate": "0.05",
    },
    {
        "code": "051910",
        "name": "LG화학",
        "market": "KOSPI",
        "sector": "화학",
        "market_cap": "20000000000000",
        "current_price": "290000",
        "change_rate": "-0.5",
        "quantity": 3,
        "average_price": "300000",
        "market_value": "870000",
        "profit_loss": "-30000",
        "profit_rate": "-0.033333",
    },
    {
        "code": "005380",
        "name": "현대차",
        "market": "KOSPI",
        "sector": "자동차",
        "market_cap": "45000000000000",
        "current_price": "210000",
        "change_rate": "0.8",
        "quantity": 4,
        "average_price": "200000",
        "market_value": "840000",
        "profit_loss": "40000",
        "profit_rate": "0.05",
    },
    {
        "code": "068270",
        "name": "셀트리온",
        "market": "KOSPI",
        "sector": "바이오",
        "market_cap": "35000000000000",
        "current_price": "170000",
        "change_rate": "-1.8",
        "quantity": 1,
        "average_price": "180000",
        "market_value": "170000",
        "profit_loss": "-10000",
        "profit_rate": "-0.055556",
    },
]


def main() -> None:
    db = SessionLocal()
    try:
        if db.query(Stock).filter(Stock.code == "005930").first() is not None:
            return

        fund_pool = FundPool(
            name="E2E 국내주식 계좌",
            currency="KRW",
            cash_balance=Decimal("5000000"),
            description="Playwright dashboard fixture",
            is_active=True,
        )
        db.add(fund_pool)
        db.flush()

        stocks: list[Stock] = []
        holdings: list[Holding] = []
        trades: list[Trade] = []
        for index, fixture in enumerate(STOCK_FIXTURES):
            stock = Stock(
                code=fixture["code"],
                name=fixture["name"],
                market=fixture["market"],
                sector=fixture["sector"],
                market_cap=Decimal(fixture["market_cap"]),
                current_price=Decimal(fixture["current_price"]),
                change_rate=Decimal(fixture["change_rate"]),
                is_favorite=index < 2,
                is_active=True,
            )
            db.add(stock)
            db.flush()
            stocks.append(stock)

            total_buy_amount = Decimal(fixture["average_price"]) * fixture["quantity"]
            holding = Holding(
                fund_pool_id=fund_pool.id,
                stock_id=stock.id,
                quantity=fixture["quantity"],
                average_price=Decimal(fixture["average_price"]),
                total_buy_amount=total_buy_amount,
                current_price=Decimal(fixture["current_price"]),
                market_value=Decimal(fixture["market_value"]),
                unrealized_profit_loss=Decimal(fixture["profit_loss"]),
                unrealized_profit_loss_rate=Decimal(fixture["profit_rate"]),
                realized_profit_loss=Decimal("25000") if index == 0 else Decimal("0"),
                first_buy_date=date(2026, 7, 1),
                last_trade_date=date(2026, 7, 8 + index),
                is_closed=False,
            )
            db.add(holding)
            holdings.append(holding)

            trade_date = date(2026, 7, 8 + index)
            trade = Trade(
                fund_pool_id=fund_pool.id,
                stock_id=stock.id,
                trade_type="buy",
                trade_date=trade_date,
                price=Decimal(fixture["average_price"]),
                quantity=fixture["quantity"],
                amount=total_buy_amount,
                fee=Decimal("0"),
                tax=Decimal("0"),
                total_amount=total_buy_amount,
                average_price_at_trade=Decimal(fixture["average_price"]),
                reason="E2E 대시보드 거래",
                memo=f"{fixture['name']} 최근 거래 메모",
                created_at=NOW - timedelta(days=6 - index),
                updated_at=NOW - timedelta(days=6 - index),
            )
            db.add(trade)
            trades.append(trade)

        db.flush()

        collection_settings = [
            StockCollectionSetting(
                stock_id=stocks[0].id,
                collect_enabled=True,
                collect_news=True,
                collect_price_snapshot=True,
                collect_alert_enabled=True,
                priority="high",
                collect_reason="holding",
            ),
            StockCollectionSetting(
                stock_id=stocks[1].id,
                collect_enabled=True,
                collect_news=True,
                collect_price_snapshot=True,
                priority="high",
                collect_reason="manual_include",
                manual_override=True,
                manual_include=True,
            ),
            StockCollectionSetting(
                stock_id=stocks[2].id,
                collect_enabled=False,
                collect_news=False,
                collect_price_snapshot=False,
                priority="low",
                collect_reason="manual_exclude",
                manual_override=True,
                manual_exclude=True,
            ),
            StockCollectionSetting(
                stock_id=stocks[3].id,
                collect_enabled=True,
                collect_news=True,
                collect_price_snapshot=True,
                priority="normal",
                collect_reason="index_rule",
            ),
            StockCollectionSetting(
                stock_id=stocks[4].id,
                collect_enabled=True,
                collect_news=True,
                collect_price_snapshot=True,
                priority="high",
                collect_reason="favorite",
            ),
            StockCollectionSetting(
                stock_id=stocks[5].id,
                collect_enabled=False,
                collect_news=False,
                collect_price_snapshot=False,
                priority="low",
            ),
        ]
        db.add_all(collection_settings)

        db.add(
            Stock(
                code="293490",
                name="카카오게임즈",
                market="KOSDAQ",
                sector="게임",
                industry="소프트웨어",
                market_cap=Decimal("2000000000000"),
                current_price=Decimal("18000"),
                change_rate=Decimal("0.3"),
                aliases_json=["카겜"],
                is_favorite=False,
                is_active=True,
            )
        )

        news_items: list[News] = []
        for index, stock in enumerate(stocks):
            published_at = NOW - timedelta(hours=5 - index)
            news = News(
                title=f"{stock.name} E2E 주요 뉴스 {index + 1}",
                url=f"https://example.com/e2e/dashboard-news-{index + 1}",
                source="E2E 경제",
                published_at=published_at,
                normalized_title=f"{stock.name} e2e 주요 뉴스 {index + 1}",
                url_hash=f"e2e-dashboard-url-{index + 1}",
                title_hash=f"e2e-dashboard-title-{index + 1}",
                news_group_key=f"e2e-dashboard-group-{index + 1}",
                source_type="manual",
                market_scope="stock",
                importance_score=8 if index == 5 else 5,
                filter_status="important_candidate" if index == 5 else "normal_candidate",
                gpt_summary_status="skipped",
                is_gpt_summary_target=False,
                is_alert_target=index == 5,
                collected_at=published_at,
                created_at=published_at,
                updated_at=published_at,
            )
            db.add(news)
            news_items.append(news)

        price_alert = PriceAlert(
            stock_id=stocks[0].id,
            alert_type="direct_price",
            target_price=Decimal("85000"),
            direction="above",
            enabled=True,
            triggered=True,
            triggered_at=NOW - timedelta(minutes=30),
            memo="E2E 가격 알림",
        )
        db.add(price_alert)
        db.flush()

        db.add(
            AlertHistory(
                stock_id=stocks[0].id,
                price_alert_id=price_alert.id,
                alert_type="price",
                recipient_email="e2e@example.com",
                title="삼성전자 목표가 접근",
                message="E2E 가격 알림 이력",
                status="sent",
                sent_at=NOW - timedelta(minutes=20),
                created_at=NOW - timedelta(minutes=20),
            )
        )

        memos: list[Memo] = []
        for index, stock in enumerate(stocks):
            memo = Memo(
                stock_id=stock.id,
                memo_type="stock",
                title=f"{stock.name} E2E 메모",
                content=f"{stock.name} 대시보드 최근 메모 내용",
                memo_date=date(2026, 7, 8 + index),
                created_at=NOW - timedelta(hours=6 - index),
                updated_at=NOW - timedelta(hours=6 - index),
            )
            db.add(memo)
            memos.append(memo)
        db.flush()

        long_term_tag = Tag(name="장기투자", color="#2563eb", tag_type="common")
        review_tag = Tag(name="실적검토", color="#dc2626", tag_type="common")
        db.add_all([long_term_tag, review_tag])
        db.flush()
        db.add_all(
            [TagLink(tag_id=long_term_tag.id, target_type="memo", target_id=memo.id) for memo in memos[:3]]
            + [TagLink(tag_id=review_tag.id, target_type="memo", target_id=memos[3].id)]
        )

        first_job = db.query(ScheduledJob).order_by(ScheduledJob.id.asc()).first()
        if first_job is not None:
            first_job.last_run_at = NOW - timedelta(hours=1)
            db.add(
                SystemLog(
                    level="info",
                    category="job_runner",
                    message="E2E 작업 성공",
                    context_json={
                        "job_id": first_job.id,
                        "job_key": first_job.job_key,
                        "status": "success",
                        "started_at": (NOW - timedelta(hours=1, minutes=1)).isoformat(),
                        "finished_at": (NOW - timedelta(hours=1)).isoformat(),
                        "message": "E2E 작업 성공",
                        "result": {},
                    },
                    created_at=NOW - timedelta(hours=1),
                )
            )

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    main()
