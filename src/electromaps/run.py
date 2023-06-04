import time

import schedule
import logging

from settings import ApiSettings, ElectromapsSettings, AllParsersSettings
from src.utils.make_request import RequestMethod, make_request
from src.utils.getting_id_places_from_db import getting_id_places_from_db

settings = ElectromapsSettings()
api_settings = ApiSettings()
time_settings = AllParsersSettings()

logger = logging.getLogger(__name__)


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
    logger.info(f'Received {len(result)} places from {settings.SOURCE_NAME}')
    return result


def _electromaps_parser():  # -> list[dict[str, int | str | float]]
    already_saved_ids = getting_id_places_from_db(settings.SOURCE_NAME)
    logger.info(f'get {len(already_saved_ids)} already saved ids from db')

    coordinates = settings.coordinates
    response = make_request(url=settings.PLACES_URL + coordinates)

    if not response:
        logger.error('can not get places')
        return

    new_parsing_places = processing_data(response.json())

    places_added = 0
    for place in new_parsing_places:
        if place['inner_id'] in already_saved_ids:
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


def electromaps_parser():
    try:
        _electromaps_parser()
    except Exception as e:
        logger.error(e)


def run() -> None:
    schedule.every().day.at(time_settings.PARSERS_START_TIME).do(electromaps_parser())
    while True:
        schedule.run_pending()
        logger.info(f"Waiting time {time_settings.SLEEP_TIME}")
        time.sleep(time_settings.SLEEP_TIME)
