import requests
from settings import ElectromapsSettings
import time

settings = ElectromapsSettings()


def request(data: str) -> dict:
    while True:
        req = requests.get(settings.URL_EM + data)
        if req.status_code == 200:
            break
        else:
            time.sleep(settings.time_sleep)
    return req.json()


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
