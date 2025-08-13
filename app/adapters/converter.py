import io

from pydub import AudioSegment


class AudioConverterAdapter:
    """Конвертер для звуков."""

    def convert_m4a_to_mp3_in_memory(self, m4a_data: io.BytesIO) -> io.BytesIO:
        """
        Converts M4A audio data (bytes) to MP3 audio data (bytes) in memory.

        Args:
            m4a_data: The M4A audio data as bytes.

        Returns:
            The converted MP3 audio data as bytes.
        """
        # Load the M4A audio from bytes
        # Use io.BytesIO to treat the bytes as a file-like object
        m4a_audio = AudioSegment.from_file(m4a_data, format="m4a")

        # Export the audio to MP3 format into a BytesIO object
        mp3_buffer = io.BytesIO()
        m4a_audio.export(mp3_buffer, format="mp3")

        return mp3_buffer
