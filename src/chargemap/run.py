import json
import time
import logging

from settings import ChargemapSettings, api_settings
from src.utils.make_request import make_request, RequestMethod

settings = ChargemapSettings()


logger = logging.getLogger(__name__)


def data_processing(response_json: dict[str, int | dict]) -> list[dict[str, int | str | float]]:
    if response_json['count'] > 0:
        result = []
        for pool in response_json['items']:
            if pool['type'] == "cluster":
                raise KeyError(f'lat = {pool["lat"]}, lng = {pool["lng"]}')
            result.append({
                'inner_id': pool['pool']['id'],
                'coordinates': {
                    'lat': pool['lat'],
                    'lng': pool['lng']
                },
                'street': pool['pool']['street_name'],
                'city': pool['pool']['city'],
                'name': pool['pool']['name'],
                'source': settings.SOURCE_NAME
                 })
        return result


def compare_and_save_id_to_database(parser_result: list[dict[str, int | str | float]]) -> None:

    places_to_database = make_request(url=api_settings.GET_LIST_ALL_PlACES + settings.SOURCE_NAME).json()
    places_set = set()

    for place in places_to_database['places']:
        for source in place['sources']:
            if source['source'] == settings.SOURCE_NAME:
                inner_id = source['inner_id']
                places_set.add(inner_id)

    for place in parser_result:
        if place['inner_id'] not in places_set:
            place_json = json.dumps(place)
            make_request(url=api_settings.POST_PLACES, data=place_json, method=RequestMethod.POST)


def chargemap_parser() -> list[dict[str, int | str | float]]:

    # Стартовые координаты левой нижней точки
    sw_lat = settings.SW_LAT
    sw_lng = settings.SW_LNG

    # Стартовые координаты правой верхней точки
    ne_lat = sw_lat + settings.DELTA
    ne_lng = sw_lng + settings.DELTA

    result = []

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
                method=RequestMethod.POST
            )

            if response is None:
                continue
            pools_data = data_processing(response.json())

            if pools_data is not None:
                result.extend(pools_data)

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

    return result


def run() -> None:
    parser_result = chargemap_parser()
    compare_and_save_id_to_database(parser_result=parser_result)

