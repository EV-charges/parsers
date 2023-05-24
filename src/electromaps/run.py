import time

import requests

from settings import ElectromapsSettings

settings = ElectromapsSettings()


def make_request(data: str) -> requests.models.Response:
    req = requests.get(settings.URL_EM + data)
    return req


def request(data: str) -> dict:
    while True:
        try:
            response = make_request(data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            time.sleep(settings.time_sleep)


def processing_data(locations_dict: dict) -> list[dict[str, int | str | float]]:
    result = []
    for location in locations_dict:
        result.append({
            'id': location['id'],
            'name': location['name'],
            'lat': location['latitude'],
            'lng': location['longitude']
        })
    return result


def electromaps_parser() -> list[dict[str, int | str | float]]:
    data = settings.LONDON_COORDINATES
    return processing_data(request(data))


def run() -> None:
    electromaps_parser()
