from pydantic import BaseModel


class PricePoint(BaseModel):
    date: str
    close: float
