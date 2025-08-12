from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Настройки приложения."""

    title: str = "Calorie-Backend"
    version: str = "0.0.1"

    users: list[int]
    token: str

    model_config = SettingsConfigDict(env_prefix="bot_")