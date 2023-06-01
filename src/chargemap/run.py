import time
import logging

from settings import ChargemapSettings
from src.utils.make_request import make_request

settings = ChargemapSettings()


logger = logging.getLogger(__name__)


def data_processing(response_json: dict[str, int | dict]) -> list[dict[str, int | str | float]]:
    if response_json['count'] > 0:
        result = []
        for pool in response_json['items']:
            if pool['type'] == "cluster":
                raise KeyError(f'lat = {pool["lat"]}, lng = {pool["lng"]}')

            result.append({
                'id': pool['pool']['id'],
                'lat': pool['lat'],
                'lng': pool['lng'],
                'street': pool['pool']['street_name'],
                'city': pool['pool']['city'],
                'name': pool['pool']['name']
                 })
        return result


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

            response = make_request(url=settings.PLACES_URL, data=data, timeout=settings.TIME_SLEEP)
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
    chargemap_parser()

