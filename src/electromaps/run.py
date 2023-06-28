import logging
import time

import schedule

from settings import AllParsersSettings, ApiSettings, ElectromapsSettings
from src.utils.getting_id_places_from_db import getting_id_places_from_db
from src.utils.make_request import RequestMethod, make_request
from src.utils.make_request_proxy import make_request_proxy

settings = ElectromapsSettings()
api_settings = ApiSettings()
time_settings = AllParsersSettings()

logger = logging.getLogger()


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


def _electromaps_parser() -> list[dict[str, int | str | float]]:
    already_saved_ids = getting_id_places_from_db(settings.SOURCE_NAME)
    logger.info(f'get {len(already_saved_ids)} already saved ids from db')

    coordinates = settings.coordinates
    response = make_request_proxy(url=settings.PLACES_URL + coordinates, retries_proxy=15, method=RequestMethod.GET)

    if not response:
        logger.error('Can not get places')
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
            allow_status_codes=(409,)
        )
        if r:
            places_added += 1

    logger.info(f'All {places_added} places added id db')


def electromaps_parser() -> None:
    try:
        _electromaps_parser()
    except Exception as e:
        logger.error(e)


def run() -> None:
    schedule.every().day.at(time_settings.PARSERS_START_TIME).do(electromaps_parser)
    while True:
        schedule.run_pending()
        time.sleep(time_settings.SLEEP_TIME)
