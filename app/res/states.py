from enum import Enum


class States(str, Enum):
    AUTH = "AUTH"
    SEND_AUDIO = "SEND_AUDIO"
