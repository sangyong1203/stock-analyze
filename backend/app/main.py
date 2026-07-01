from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.domains.alerts.router import router as alerts_router
from app.domains.auth.router import router as auth_router
from app.domains.charts.router import router as charts_router
from app.domains.collection.router import router as collection_router
from app.domains.dashboard.router import router as dashboard_router
from app.domains.funds.router import router as funds_router
from app.domains.holdings.router import router as holdings_router
from app.domains.jobs.router import router as jobs_router
from app.domains.memos.router import router as memos_router
from app.domains.news.router import router as news_router
from app.domains.portfolio.router import router as portfolio_router
from app.domains.prices.router import router as prices_router
from app.domains.settings.router import router as settings_router
from app.domains.stocks.router import router as stocks_router
from app.domains.tags.router import router as tags_router
from app.domains.trades.router import router as trades_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)
    allowed_origins = [origin.strip() for origin in settings.allowed_origins.split(",") if origin.strip()]
    if settings.allowed_origin and settings.allowed_origin not in allowed_origins:
        allowed_origins.append(settings.allowed_origin)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
    app.include_router(dashboard_router, prefix="/api/dashboard", tags=["dashboard"])
    app.include_router(jobs_router, prefix="/api/jobs", tags=["jobs"])
    app.include_router(stocks_router, prefix="/api/stocks", tags=["stocks"])
    app.include_router(collection_router, prefix="/api/collection", tags=["collection"])
    app.include_router(news_router, prefix="/api/news", tags=["news"])
    app.include_router(funds_router, prefix="/api/funds", tags=["funds"])
    app.include_router(holdings_router, prefix="/api/holdings", tags=["holdings"])
    app.include_router(portfolio_router, prefix="/api/portfolio", tags=["portfolio"])
    app.include_router(trades_router, prefix="/api/trades", tags=["trades"])
    app.include_router(alerts_router, prefix="/api/price-alerts", tags=["price-alerts"])
    app.include_router(prices_router, prefix="/api/prices", tags=["prices"])
    app.include_router(charts_router, prefix="/api/charts", tags=["charts"])
    app.include_router(memos_router, prefix="/api/memos", tags=["memos"])
    app.include_router(tags_router, prefix="/api/tags", tags=["tags"])
    app.include_router(settings_router, prefix="/api/settings", tags=["settings"])
    return app


app = create_app()
