import time
from enum import StrEnum, auto
from logging import getLogger

import requests

logger = getLogger(__name__)


class RequestMethod(StrEnum):
    GET = auto()
    POST = auto()


def make_request(
        url: str,
        method: str = RequestMethod.GET,
        timeout: float = 10,
        retries: int = 2,
        sleep_time: float = 1,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        proxy: dict | None = None
) -> requests.Response | None:
    try:
        r = requests.request(
            method=method,
            url=url,
            data=data,
            timeout=timeout,
            params=params,
            json=json,
            proxies=proxy
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
                json=json,
                params=params,
                proxy=proxy
            )
        logger.info(f'Failed to make request to {method.upper()} {url}')
        return None
    return r
