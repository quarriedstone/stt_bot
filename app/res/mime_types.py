from enum import Enum


class MimeTypes(str, Enum):
    m4a = "audio/x-m4a"
    mp3 = "audio/mpeg"
    ogg = "audio/ogg"
    wav = "audio/x-wav"
