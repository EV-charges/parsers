from logging import getLogger

import requests
from fake_useragent import UserAgent

from settings import AllParsersSettings
from src.utils.make_request import RequestMethod, make_request

settings = AllParsersSettings()
logger = getLogger(__name__)


def make_request_proxy(
        url: str,
        method: str = RequestMethod.POST,
        timeout: float = 10,
        retries: int = 0,
        sleep_time: float = 1,
        retries_proxy: int = 2,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
) -> requests.Response | None:
    proxy = None
    headers = None

    if settings.IS_DEBUG:
        while True:
            proxy_server_response = make_request(url=settings.PROXYPOOL_URL)
            if proxy_server_response is None:
                logger.error(f'Failed to make request to proxy')
                return None
            proxy_ip = proxy_server_response.json().get('proxy')
            if proxy_ip:
                break

        proxy = {
            'http': 'http://' + proxy_ip,
            'https': 'http://' + proxy_ip
        }

        user_agent = UserAgent().random
        headers = {
            'accept': '*/*',
            'user-agent': user_agent
        }

    response = make_request(
        url=url,
        method=method,
        timeout=timeout,
        retries=retries,
        sleep_time=sleep_time,
        data=data,
        json=json,
        params=params,
        proxy=proxy,
        headers=headers
    )
    if response is None:
        if retries_proxy > 0:
            return make_request_proxy(
                url=url,
                method=method,
                timeout=timeout,
                retries=retries,
                sleep_time=sleep_time,
                data=data,
                json=json,
                params=params,
                retries_proxy=retries_proxy - 1
            )
        return None
    return response
