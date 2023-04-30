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


class Settings(BaseSettings):

    class Config:
        case_sensitive = False
