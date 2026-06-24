from pydantic import BaseModel


class OpenAiTextResult(BaseModel):
    text: str
    model: str
