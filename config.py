import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    deepseek_api_key: str
    deepseek_base_url: str
    deepseek_model: str
    request_timeout_seconds: float
    max_tokens: int
    temperature: float
    max_input_chars: int
    flask_host: str
    flask_port: int
    flask_debug: bool


def _to_bool(value: str, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def load_settings() -> Settings:
    return Settings(
        deepseek_api_key=os.getenv("DEEPSEEK_API_KEY", "").strip(),
        deepseek_base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").strip(),
        deepseek_model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat").strip(),
        request_timeout_seconds=float(os.getenv("REQUEST_TIMEOUT_SECONDS", "40")),
        max_tokens=int(os.getenv("MAX_TOKENS", "1800")),
        temperature=float(os.getenv("TEMPERATURE", "0.7")),
        max_input_chars=int(os.getenv("MAX_INPUT_CHARS", "2000")),
        flask_host=os.getenv("FLASK_HOST", "0.0.0.0").strip(),
        flask_port=int(os.getenv("FLASK_PORT", "5000")),
        flask_debug=_to_bool(os.getenv("FLASK_DEBUG"), default=True),
    )
