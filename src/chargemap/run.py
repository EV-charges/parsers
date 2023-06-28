import logging
import time

import schedule

from settings import AllParsersSettings, ApiSettings, ChargemapSettings
from src.utils.chargemap_classes import Point, ScanSquare
from src.utils.getting_id_places_from_db import getting_id_places_from_db
from src.utils.make_request import RequestMethod, make_request
from src.utils.make_request_proxy import make_request_proxy

settings = ChargemapSettings()
api_settings = ApiSettings()
time_settings = AllParsersSettings()
logger = logging.getLogger()


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
    sw_point = Point(lat=settings.SW_LAT, lng=settings.SW_LNG)

    ne_lat = sw_point.lat + settings.DELTA
    ne_lng = sw_point.lng + settings.DELTA
    ne_point = Point(lat=ne_lat, lng=ne_lng)

    scan_square = ScanSquare(sw_point, ne_point)

    places_id_set = getting_id_places_from_db(source_name=settings.SOURCE_NAME)
    logger.info(f'get {len(places_id_set)} places from db')
    count_add_places = 0
    good_request = 0
    count_request = 0

    # Цикл сканирования
    while scan_square.upper_border_check():
        while scan_square.right_border_check():
            data = {
                "city": "London",
                "NELat": scan_square.ne_lat,
                "NELng": scan_square.ne_lng,
                "SWLat": scan_square.sw_lat,
                "SWLng": scan_square.sw_lng
            }
            count_request += 1

            response = make_request_proxy(
                url=settings.PLACES_URL,
                data=data,
                sleep_time=settings.TIME_SLEEP,
                method=RequestMethod.POST,
            )

            if response is None:
                scan_square.move_to_the_right()
                time.sleep(settings.TIME_SLEEP)
                continue
            good_request += 1

            count_add_places += data_processing_and_save_db(response.json(), places_id_set)

            # Сдвигаемся вправо
            scan_square.move_to_the_right()
            time.sleep(settings.TIME_SLEEP)

        # Поднимаемся наверх
        scan_square.move_to_the_top()

        # Возвращаемся в начало строки
        scan_square.returning_to_the_beginning_of_the_line()

    logger.info(f'{count_add_places} places sent to the database')
    logger.info(f'successful requests {good_request}/{count_request}')


def chargemap_parser() -> None:
    try:
        _chargemap_parser()
    except Exception as e:
        logger.error(e)


def run() -> None:
    schedule.every().day.at(time_settings.PARSERS_START_TIME).do(chargemap_parser)
    while True:
        schedule.run_pending()
