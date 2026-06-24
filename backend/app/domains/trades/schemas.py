from pydantic import BaseModel


class TradeSummary(BaseModel):
    id: int
    trade_type: str
