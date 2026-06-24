"""add named unique indexes

Revision ID: 20260624_0002
Revises: 20260624_0001
Create Date: 2026-06-24
"""

from alembic import op

revision = "20260624_0002"
down_revision = "20260624_0001"
branch_labels = None
depends_on = None


def _index_exists(index_name: str) -> bool:
    bind = op.get_bind()
    return bool(
        bind.exec_driver_sql(
            "SELECT 1 FROM sqlite_master WHERE type = 'index' AND name = ?",
            (index_name,),
        ).first()
    )


def _create_unique_index(index_name: str, table_name: str, columns: list[str]) -> None:
    if not _index_exists(index_name):
        op.create_index(index_name, table_name, columns, unique=True)


def upgrade() -> None:
    _create_unique_index("uq_app_settings_key", "app_settings", ["setting_key"])
    _create_unique_index("uq_scheduled_jobs_key", "scheduled_jobs", ["job_key"])
    _create_unique_index("uq_stocks_code", "stocks", ["code"])
    _create_unique_index("uq_index_constituents_unique", "index_constituents", ["index_code", "stock_code", "effective_date"])
    _create_unique_index("uq_stock_prices_stock_date_timeframe", "stock_prices", ["stock_id", "date", "timeframe"])
    _create_unique_index("uq_stock_collection_stock", "stock_collection_settings", ["stock_id"])
    _create_unique_index("uq_news_url_hash", "news", ["url_hash"])
    _create_unique_index("uq_news_keyword_group_keyword", "news_keyword_settings", ["group_type", "keyword"])
    _create_unique_index("uq_tags_name_type", "tags", ["name", "tag_type"])


def downgrade() -> None:
    op.drop_index("uq_tags_name_type", table_name="tags")
    op.drop_index("uq_news_keyword_group_keyword", table_name="news_keyword_settings")
    op.drop_index("uq_news_url_hash", table_name="news")
    op.drop_index("uq_stock_collection_stock", table_name="stock_collection_settings")
    op.drop_index("uq_stock_prices_stock_date_timeframe", table_name="stock_prices")
    op.drop_index("uq_index_constituents_unique", table_name="index_constituents")
    op.drop_index("uq_stocks_code", table_name="stocks")
    op.drop_index("uq_scheduled_jobs_key", table_name="scheduled_jobs")
    op.drop_index("uq_app_settings_key", table_name="app_settings")
