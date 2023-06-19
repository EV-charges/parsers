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
        data: dict = None,
        method: str = RequestMethod.GET,
        timeout: float = 10,
        retries: int = 2,
        sleep_time: float = 1,
        json: dict = None,
        params: dict = None,
        proxy: dict = None,
        headers: dict = None,
        allow_status_codes: tuple[int, ...] = None
) -> requests.Response | None:
    try:
        r = requests.request(
            method=method,
            url=url,
            data=data,
            timeout=timeout,
            params=params,
            json=json,
            proxies=proxy,
            headers=headers
        )
        if allow_status_codes and r.status_code in allow_status_codes:
            return

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
                proxy=proxy,
                headers=headers
            )
        logger.info(f'Failed to make request to {method.upper()} {url}')
        return None
    return r
