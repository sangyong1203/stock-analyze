from pydantic import BaseModel


class MemoSummary(BaseModel):
    memo_type: str
    title: str | None = None
