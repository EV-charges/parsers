from settings import ElectromapsSettings
from src.utils.make_request import make_request

settings = ElectromapsSettings()


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
    coordinates = settings.coordinates
    response = make_request(url=settings.PLACES_URL + coordinates)
    return processing_data(response.json())


def run() -> None:
    electromaps_parser()
