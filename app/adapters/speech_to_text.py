from dataclasses import dataclass
from io import BytesIO

from transformers import pipeline


@dataclass
class SttAdapter:
    """Адаптер для перевода звуковой дорожки в текст."""

    _model_name: str
    _chunk_length: int = 30

    def __post_init__(self):
        self._pipe = pipeline(
            "automatic-speech-recognition",
            model=self._model_name,
            chunk_length_s=self._chunk_length,
        )

    def stt_to_text(
        self,
        audio: BytesIO,
    ):
        """Преобразовать аудио в текст."""
        result = self._pipe(audio.getvalue())
        return result["text"]
