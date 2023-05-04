import requests
from parsers.settings import ElectromapsSettings

settings = ElectromapsSettings()


def request(data: dict):
    req = requests.post(settings.URL_EM, json=data)
    return req.json()


def processing_data(locations_dict) -> list[dict[str, int | str | float]]:
    result = []
    for location in locations_dict:
        result.append({
            'id': location['id'],
            'name': location['name'],
            'lat': location['latitude'],
            'lng': location['longitude']
        })
    return result


def electromaps_parser():
    data = settings.LONDON_COORDINATES
    return processing_data(request(data))


def run() -> None:
    electromaps_parser()