from pydantic import BaseModel


class AlertSummary(BaseModel):
    enabled: bool = True
