from enum import StrEnum, auto
from pathlib import Path

import dotenv
from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = Path(BASE_DIR, '.env')
dotenv.load_dotenv(ENV_FILE)


class ParserType(StrEnum):
    chargemap = auto()
    plugshare = auto()


PARSERS_TYPES = [pt.value for pt in ParserType]


class ChargemapSettings(BaseSettings):
    URL_CM: str
    TIME_SLEEP: int

    NE_LAT_CM: float
    NE_LNG_CM: float

    SW_LAT_CM: float
    SW_LNG_CM: float

    LAT_DELTA_CM: float
    LNG_DELTA_CM: float


class Settings(ChargemapSettings):

    class Config:
        case_sensitive = False


settings = Settings()

