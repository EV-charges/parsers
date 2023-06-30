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
    def coordinates(self) -> dict:
        return {
            'latNE': self.NE_LAT,
            'lngNE': self.NE_LNG,
            'latSW': self.SW_LAT,
            'lngSW': self.SW_LNG
            }

    LIMIT: int = 100
    OFFSET: int = 0

    URL_GET_TOKEN = 'https://cognito-idp.eu-west-1.amazonaws.com/'

    HEADERS_GET_TOKEN = {
        "content-type": "application/x-amz-json-1.1",
        "referer": "https://map.electromaps.com/",
        "x-amz-target": "AWSCognitoIdentityProviderService.InitiateAuth",
    }

    USERNAME: str = 'testoviytest22121@gmail.com'
    PASSWORD: str = 'Sobaka12'

    @property
    def json_get_token(self) -> dict:
        json_get_token = {
            "AuthFlow": "USER_PASSWORD_AUTH",
            "ClientId": "539ogq18bspa4d1v2bi01g5c01",
            "AuthParameters": {
                "USERNAME": self.USERNAME,
                "PASSWORD": self.PASSWORD
            },
            "ClientMetadata": {}
        }
        return json_get_token

    TIME_SLEEP = 1
    SOURCE_NAME: str = 'electromaps'

    class Config:
        case_sensitive = False
        env_prefix = "ELECTROMAPS_"


class ApiSettings(BaseSettings):
    BASE_URL: str = 'http://209.38.204.96:8080/api/v1'

    @property
    def get_or_post_places_url(self) -> str:
        return f'{self.BASE_URL}/places'

    @property
    def post_comments_url(self) -> str:
        return f'{self.BASE_URL}/comments'

    NUMBER_RECORDS_IN_ONE_QUERY: int = 100


class AllParsersSettings(BaseSettings):
    PROXYPOOL_URL: str = 'http://127.0.0.1:5010/get?type=https'
    PARSERS_START_TIME: str = '12:00'
    SLEEP_TIME: int = 1
    IS_DEBUG: bool = True


class Settings(BaseSettings):
    class Config:
        case_sensitive = False
