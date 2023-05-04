import time

import requests
from parsers.settings import ChargemapSettings

settings = ChargemapSettings()


def request(data: dict[str, str | float]) -> dict[str, int | dict] | None:
    try:
        response = requests.post(settings.URL_CM, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None


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
    sw_lat = settings.SW_LAT_CM
    sw_lng = settings.SW_LNG_CM

    # Стартовые координаты правой верхней точки
    ne_lat = sw_lat + settings.DELTA_CM
    ne_lng = sw_lng + settings.DELTA_CM

    result = []

    # Цикл сканирования
    while sw_lat <= settings.NE_LAT_CM:
        while sw_lng <= settings.NE_LNG_CM:
            data = {
                    "city": "London",
                    "NELat": ne_lat,
                    "NELng": ne_lng,
                    "SWLat": sw_lat,
                    "SWLng": sw_lng
                    }

            response_json = request(data)

            if response_json is None:
                time.sleep(settings.TIME_SLEEP)
                continue

            pools_data = data_processing(response_json)

            if pools_data is not None:
                result.extend(pools_data)

            # Сдвигаемся вправо
            ne_lng += settings.DELTA_CM
            sw_lng += settings.DELTA_CM
            time.sleep(settings.TIME_SLEEP)

        # Поднимаемся наверх
        ne_lat += settings.DELTA_CM
        sw_lat += settings.DELTA_CM

        # Возвращаемся в начало строки
        sw_lng = settings.SW_LNG_CM
        ne_lng = sw_lng + settings.DELTA_CM

    return result


def run() -> None:
    chargemap_parser()

