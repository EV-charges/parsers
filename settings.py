from enum import StrEnum, auto
from pathlib import Path

import dotenv
from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = Path(BASE_DIR, '.env')
dotenv.load_dotenv(ENV_FILE)


class ParserType(StrEnum):
    chargemap = auto()
    electromaps = auto()


PARSERS_TYPES = [pt.value for pt in ParserType]


class ChargemapSettings(BaseSettings):
    PLACES_URL: str = 'https://chargemap.com/json/charging/pools/get_from_areas'
    TIME_SLEEP: int = 1

    NE_LAT: float = 51.74
    NE_LNG: float = 0.4
    SW_LAT: float = 51.05
    SW_LNG: float = -0.7

    DELTA: float = 0.06
    SOURCE_NAME: str = 'chargemap'


class ElectromapsSettings(BaseSettings):
    PLACES_URL: str = 'https://www.electromaps.com/mapi/v2/locations'

    NE_LAT: float = 51.74
    NE_LNG: float = 0.4
    SW_LAT: float = 51.05
    SW_LNG: float = -0.7

    @property
    def coordinates(self) -> str:
        return f'?latNE={self.NE_LAT}&lngNE={self.NE_LNG}&latSW={self.SW_LAT}&lngSW={self.SW_LNG}'

    LIMIT = 10
    OFFSET = 0

    HEADERS = {
        'X-Em-Oidc-Accesstoken': 'pass',
        'X-Em-Oidc-Data': 'pass'
    }

    def comments(
            self,
            place_id: int,
            limit: int,
            offset: int
    ) -> str:
        return f'/{place_id}/comments?limit={limit}&offset={offset}'

    TIME_SLEEP = 1
    SOURCE_NAME: str = 'electromaps'


class ApiSettings(BaseSettings):
    GET_LIST_ALL_PlACES = 'http://209.38.204.96:8080/api/v1/places'
    POST_PLACES = 'http://209.38.204.96:8080/api/v1/places'
    POST_COMMENTS = 'http://209.38.204.96:8080/api/v1/comments'
    NUMBER_RECORDS_IN_ONE_QUERY: int = 100


class AllParsersSettings(BaseSettings):
    PARSERS_START_TIME: str = '12:00'
    SLEEP_TIME: int = 1


class Settings(BaseSettings):
    class Config:
        case_sensitive = False


