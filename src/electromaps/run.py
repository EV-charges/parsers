import schedule
import logging

from settings import ApiSettings, ElectromapsSettings
from src.utils.make_request import RequestMethod, make_request
from src.utils.getting_id_places_from_db import getting_id_places_from_db

settings = ElectromapsSettings()
api_settings = ApiSettings()

logger = logging.getLogger(__name__)


# TODO: add scheduling; every day at 12:00
# TODO: add additional logging


def processing_data(
        locations_dict: list[dict]
) -> list[dict[str, int | str | float]]:
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
    logger.info(f'get {len(already_saved_id)} already saved ids from db')

    coordinates = settings.coordinates
    response = make_request(url=settings.PLACES_URL + coordinates)
    if not response:
        logger.error('can not get places')
        return

    new_parsing_places = processing_data(response.json())

    places_added = 0
    for place in new_parsing_places[:100]:
        if place['inner_id'] in already_saved_id:
            continue

        r = make_request(
            url=api_settings.POST_PLACES,
            json=place,
            method=RequestMethod.POST,
            allow_satus_codes=(409,)
        )
        if r:
            places_added += 1

    logger.info(f'{places_added} places added id db')


def run() -> None:
    try:
        electromaps_parser()
    except Exception as e:  # noqa
        logger.error(e)
