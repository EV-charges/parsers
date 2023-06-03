import schedule

from settings import ApiSettings, ElectromapsSettings
from src.utils.make_request import RequestMethod, make_request
from src.utils.setup_logging import setup_logging
from src.utils.getting_id_places_from_db import getting_id_places_from_db

settings = ElectromapsSettings()
api_settings = ApiSettings()


def processing_data(locations_dict: dict) -> list[dict[str, int | str | float]]:
    result = []
    for location in locations_dict:
        result.append({
            'inner_id': location['id'],
            'coordinates': {
                'lat': location['latitude'],
                'lng': location['longitude']
            },
            'name': location['name'],
            'source': settings.SOURCE_NAME

        })
    return result


def electromaps_parser():  # -> list[dict[str, int | str | float]]
    already_saved_id = getting_id_places_from_db(settings.SOURCE_NAME)

    coordinates = settings.coordinates
    response = make_request(url=settings.PLACES_URL + coordinates)
    new_parsing_places = processing_data(response.json())
    for place in new_parsing_places:
        if place['inner_id'] not in already_saved_id:
            make_request(url=api_settings.POST_PLACES, data=place, method=RequestMethod.POST)


def run() -> None:
    electromaps_parser()
