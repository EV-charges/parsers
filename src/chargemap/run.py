import logging
import time

from settings import ChargemapSettings, api_settings
from src.utils.getting_id_places_from_db import getting_id_places_from_db
from src.utils.make_request import RequestMethod, make_request

settings = ChargemapSettings()

logger = logging.getLogger(__name__)
proxy = {
    "http": "http://7S3gTR:DQy9zH@185.240.94.231:8000",
    "https": "http://7S3gTR:DQy9zH@185.240.94.231:8000"
}


def data_processing_and_save_db(response_json: dict[str, int | dict], places_id_set:set[int]) -> int:
    count_add_places = 0
    try:
        if response_json['count'] > 0:
            for pool in response_json['items']:
                if pool['type'] == "cluster":
                    raise KeyError(f'Incorrect scale lat = {pool["lat"]}, lng = {pool["lng"]}')
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
                if response is not None:
                    count_add_places += 1

    except KeyError as e:
        logger.error(e)

    return count_add_places


def chargemap_parser() -> None:
    # Стартовые координаты левой нижней точки
    sw_lat = settings.SW_LAT
    sw_lng = settings.SW_LNG

    # Стартовые координаты правой верхней точки
    ne_lat = sw_lat + settings.DELTA
    ne_lng = sw_lng + settings.DELTA

    places_id_set = getting_id_places_from_db(source_name=settings.SOURCE_NAME)
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
                proxy=proxy
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


def run() -> None:
    chargemap_parser()
