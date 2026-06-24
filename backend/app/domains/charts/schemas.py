from pydantic import BaseModel


class ChartSummary(BaseModel):
    timeframe: str = "daily"
