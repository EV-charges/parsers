import time
from typing import List, Dict
import requests

URL = "https://chargemap.com/json/charging/pools/get_from_areas"

# Координаты крайней правой верхней точки
NE_LAT = 51.73723455
NE_LNG = 0.35

# Координаты начальной левой нижней точки
SW_LAT = 51.05175436
SW_LNG = -0.65

# Значения шага
lat_delta = 0.02136975
lng_delta = 0.12574196


def chargemap_parser() -> List[Dict]:

    # Стартовые координаты левой нижней точки
    sw_lat = SW_LAT
    sw_lng = SW_LNG

    # Стартовые координаты правой верхней точки
    ne_lat = sw_lat + lat_delta
    ne_lng = sw_lng + lng_delta

    result = []

    # Цикл сканирования
    while sw_lat <= NE_LAT:
        while sw_lng <= NE_LNG:
            data = {
                    "city": "London",
                    "NELat": ne_lat,
                    "NELng": ne_lng,
                    "SWLat": sw_lat,
                    "SWLng": sw_lng
                    }

            response = requests.post(URL, data=data)
            json_response = response.json()

            if json_response['count'] > 0:
                for pool in json_response['items']:
                    result.append({
                        'id': pool['pool']['id'],
                        'lat': pool['lat'],
                        'lng': pool['lng'],
                        'street': pool['pool']['name']

                    })

            # Сдвигаемся вправо
            ne_lng += lng_delta
            sw_lng += lng_delta
            time.sleep(1)

        # Поднимаемся наверх
        ne_lat += lat_delta
        sw_lat += lat_delta

        # Возвращаемся в начало строки
        sw_lng = SW_LNG
        ne_lng = sw_lng + lng_delta

    return result

def run() -> None:
    pass
