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
    URL_CM: str = 'https://chargemap.com/json/charging/pools/get_from_areas'
    TIME_SLEEP: int = 1

    NE_LAT_CM: float = 51.73723455
    NE_LNG_CM: float = 0.35

    SW_LAT_CM: float = 51.05175436
    SW_LNG_CM: float = -0.65

    DELTA_CM: float = 0.06


class Settings(BaseSettings):

    class Config:
        case_sensitive = False



