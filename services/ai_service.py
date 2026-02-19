from pathlib import Path
from typing import Optional

from openai import OpenAI

from config import Settings


class DeepSeekHealthAdvisor:
    def __init__(self, settings: Settings, prompt_file: Path):
        self._settings = settings
        self._prompt_template = prompt_file.read_text(encoding="utf-8")
        self._client: Optional[OpenAI] = None

        if settings.deepseek_api_key:
            self._client = OpenAI(
                api_key=settings.deepseek_api_key,
                base_url=settings.deepseek_base_url,
                timeout=settings.request_timeout_seconds,
            )

    @property
    def is_ready(self) -> bool:
        return self._client is not None

    def _build_prompt(self, user_input: str) -> str:
        return self._prompt_template.replace("{{USER_INPUT}}", user_input)

    def generate_advice(self, user_input: str) -> str:
        if not self._client:
            raise RuntimeError("DeepSeek client is not configured. Missing DEEPSEEK_API_KEY.")

        response = self._client.chat.completions.create(
            model=self._settings.deepseek_model,
            messages=[{"role": "user", "content": self._build_prompt(user_input)}],
            max_tokens=self._settings.max_tokens,
            temperature=self._settings.temperature,
            stream=False,
        )

        content = (
            response.choices[0].message.content
            if response.choices and response.choices[0].message
            else None
        )
        return (content or "抱歉，未能获取有效建议。").strip()
