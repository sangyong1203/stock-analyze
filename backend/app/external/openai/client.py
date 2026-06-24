import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.external.openai.types import OpenAiTextResult


class OpenAiNewsClient:
    endpoint = "https://api.openai.com/v1/responses"

    def __init__(self, api_key: str, timeout: int = 30) -> None:
        self.api_key = api_key
        self.timeout = timeout

    def create_text_response(self, model: str, prompt: str) -> OpenAiTextResult:
        payload = {
            "model": model,
            "input": prompt,
        }
        request = Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            message = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenAI API error {exc.code}: {message}") from exc
        except URLError as exc:
            raise RuntimeError(f"OpenAI API request failed: {exc.reason}") from exc

        text = self._extract_text(data)
        if not text:
            raise RuntimeError("OpenAI API response did not include output text")
        return OpenAiTextResult(text=text, model=model)

    @staticmethod
    def _extract_text(data: dict) -> str:
        if isinstance(data.get("output_text"), str):
            return data["output_text"].strip()

        parts: list[str] = []
        for output in data.get("output", []) or []:
            for content in output.get("content", []) or []:
                if content.get("type") in {"output_text", "text"} and isinstance(content.get("text"), str):
                    parts.append(content["text"])
        return "\n".join(part.strip() for part in parts if part.strip())
