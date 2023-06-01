import time
from enum import StrEnum, auto
from logging import getLogger

import requests
from pydantic.types import Json

logger = getLogger(__name__)


class RequestMethod(StrEnum):
    GET = auto()
    POST = auto()


def make_request(
        url: str,
        data: dict | Json = None,
        method: str = RequestMethod.GET,
        timeout: float = 10,
        retries: int = 2,
        sleep_time: float = 1,
) -> requests.Response | None:
    try:
        r = requests.request(
            method=method,
            url=url,
            data=data,
            timeout=timeout,
        )
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(e)
        if retries > 0:
            time.sleep(sleep_time)
            return make_request(
                url=url,
                data=data,
                method=method,
                timeout=timeout,
                retries=retries - 1,
            )
        logger.info(f'Failed to make request to {method.upper()} {url}')
        return None
    return r
