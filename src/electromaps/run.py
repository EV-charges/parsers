import requests
from parsers.settings import ElectromapsSettings
import time
settings = ElectromapsSettings()


def request(data: dict) -> dict:
    try:
        req = requests.post(settings.URL_EM, json=data)
        return req.json()
    except Exception:
        time.sleep(15)
        req = requests.post(settings.URL_EM, json=data)
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
