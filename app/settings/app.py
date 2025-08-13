from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Настройки приложения."""

    title: str = "Calorie-Backend"
    version: str = "0.0.1"

    users: list[int]
    token: str

    chunk_size: int = 4096
    model_path: str = "openai/whisper-medium"

    model_config = SettingsConfigDict(env_prefix="bot_")
