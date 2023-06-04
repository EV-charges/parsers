import logging
import time

import schedule

from settings import AllParsersSettings, ApiSettings, ChargemapSettings
from src.utils.getting_id_places_from_db import getting_id_places_from_db
from src.utils.make_request import RequestMethod, make_request

settings = ChargemapSettings()
api_settings = ApiSettings()
time_settings = AllParsersSettings()
logger = logging.getLogger(__name__)


def data_processing_and_save_db(response_json: dict[str, int | dict], places_id_set: set[int]) -> int:
    count_add_places = 0
    if response_json['count'] > 0:
        for pool in response_json['items']:

            if pool['type'] == 'cluster':
                logger.error(f"Incorrect scale lat = {pool['lat']}, lng = {pool['lng']}")
                continue

            if pool['pool']['id'] in places_id_set:
                continue

            place = {
                'inner_id': pool['pool']['id'],
                'coordinates': {
                    'lat': pool['lat'],
                    'lng': pool['lng']
                },
                'street': pool['pool']['street_name'],
                'city': pool['pool']['city'],
                'name': pool['pool']['name'],
                'source': settings.SOURCE_NAME
            }

            response = make_request(url=api_settings.POST_PLACES, json=place, method=RequestMethod.POST)
            if response:
                count_add_places += 1

    return count_add_places


def _chargemap_parser() -> None:
    # Стартовые координаты левой нижней точки
    sw_lat = settings.SW_LAT
    sw_lng = settings.SW_LNG

    # Стартовые координаты правой верхней точки
    ne_lat = sw_lat + settings.DELTA
    ne_lng = sw_lng + settings.DELTA

    places_id_set = getting_id_places_from_db(source_name=settings.SOURCE_NAME)
    logger.info(f'get {len(places_id_set)} places from db')
    count_add_places = 0

    # Цикл сканирования
    while sw_lat <= settings.NE_LAT:
        while sw_lng <= settings.NE_LNG:
            data = {
                "city": "London",
                "NELat": ne_lat,
                "NELng": ne_lng,
                "SWLat": sw_lat,
                "SWLng": sw_lng
            }

            response = make_request(
                url=settings.PLACES_URL,
                data=data,
                timeout=settings.TIME_SLEEP,
                method=RequestMethod.POST,
            )

            if response is None:
                continue

            count_add_places += data_processing_and_save_db(response.json(), places_id_set)

            # Сдвигаемся вправо
            ne_lng += settings.DELTA
            sw_lng += settings.DELTA
            time.sleep(settings.TIME_SLEEP)

        # Поднимаемся наверх
        ne_lat += settings.DELTA
        sw_lat += settings.DELTA

        # Возвращаемся в начало строки
        sw_lng = settings.SW_LNG
        ne_lng = sw_lng + settings.DELTA

    logger.info(f'{count_add_places} places sent to the database')


def chargemap_parser() -> None:
    try:
        _chargemap_parser()
    except Exception as e:
        logger.error(e)


def run() -> None:
    schedule.every().day.at(time_settings.PARSERS_START_TIME).do(chargemap_parser)
    while True:
        schedule.run_pending()
