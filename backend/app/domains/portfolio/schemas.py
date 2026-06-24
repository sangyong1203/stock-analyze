from pydantic import BaseModel


class PortfolioSummary(BaseModel):
    cash_balance: float = 0
    market_value: float = 0
