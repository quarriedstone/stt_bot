from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Provider

from app.adapters.converter import AudioConverterAdapter
from app.adapters.speech_to_text import SttAdapter
from app.settings.app import AppSettings


class AppContainer(DeclarativeContainer):
    """Контейнер с зависимостями."""

    app_settings: Provider[AppSettings] = Singleton(AppSettings)

    stt_adapter: Singleton[SttAdapter] = Singleton(
        SttAdapter,
        app_settings.provided.model_path,
    )

    audio_adapter: Singleton[AudioConverterAdapter] = Singleton(AudioConverterAdapter)


APP_CONTAINER = AppContainer()
