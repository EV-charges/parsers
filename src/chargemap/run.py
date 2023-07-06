import logging
import re
import time

import schedule
from requests import Session

from settings import AllParsersSettings, ChargemapSettings
from src.utils.chargemap_classes import Point, ScanSquare
from src.utils.getting_id_places_from_db import getting_id_places_from_db
from src.utils.make_request import RequestMethod
from src.utils.make_request_proxy import make_request_proxy
from src.utils.uploading_db_functions import uploading_comments, uploading_places

settings = ChargemapSettings()
time_settings = AllParsersSettings()
logger = logging.getLogger(__name__)


def processing_places_and_save_db(
        response_json: dict[str, int | dict],
        places_id_set: set[int]
) -> int:
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

            response = uploading_places(place)

            if response:
                count_add_places += 1

    return count_add_places


def get_access_token() -> dict | str:
    headers = settings.HEADERS_GET_TOKEN
    data = settings.json_get_token

    work = Session()
    authorization = work.post(
        url=settings.AUTHORIZATION_URL,
        headers=headers,
        data=data
    )

    if not authorization:
        return "Can't authorization"

    r = work.get(settings.URL_GET_TOKEN,
                 headers=headers)

    match = re.search(settings.RE_PATTERN_GET_TOKEN, r.text)
    if not match:
        return "Can't get token"
    user_token = match.group(1)

    access_token_headers = {
        'Authorization': user_token
    }

    return access_token_headers


def comments_parsing(headers: dict) -> dict:
    places_ids = getting_id_places_from_db(settings.SOURCE_NAME)

    result = {}
    for place_id in places_ids:
        limit = settings.LIMIT
        offset = settings.OFFSET
        place_comments = []

        while True:
            url = settings.COMMENTS_URL
            resp = make_request_proxy(
                url=url,
                headers=headers,
                params={
                    'pool_id': place_id,
                    'offset': offset,
                    'limit': limit
                },
                method=RequestMethod.GET
            )
            if not resp:
                break
            resp = resp.json()
            comments = resp['items']

            if not comments:
                break

            place_comments.extend(comments)
            offset += limit

        result[place_id] = place_comments
    return result


def processing_comments(
        places_comments: dict[int, list]
) -> list[dict]:
    result = []

    for place_id, comments in places_comments.items():
        for comment in comments:
            result.append({
                'place_id': place_id,
                'comment_id': comment['id'],
                'author': comment['user_username'],
                'text': comment.get('comment', 'No text'),
                'publication_date': comment['creation_date'],
                'source': 'chargemap'
            })
    return result


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
                "city": "Barcelona",
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

            count_add_places += processing_places_and_save_db(response.json(), places_id_set)

            # Сдвигаемся вправо
            scan_square.move_to_the_right()
            time.sleep(settings.TIME_SLEEP)

        # Поднимаемся наверх
        scan_square.move_to_the_top()

        # Возвращаемся в начало строки
        scan_square.returning_to_the_beginning_of_the_line()

    logger.info(f'{count_add_places} places sent to the database')
    logger.info(f'successful requests {good_request}/{count_request}')

    access_token = get_access_token()
    places_comments = comments_parsing(access_token)
    comments = processing_comments(places_comments)

    comments_added = 0
    for comment in comments:

        comment_add = uploading_comments(comment)
        if comment_add:
            comments_added += 1

    logger.info(f'All {comments_added} comments added in db')


def chargemap_parser() -> None:
    try:
        _chargemap_parser()
    except Exception as e:
        logger.error(e)


def run() -> None:
    schedule.every().day.at(time_settings.PARSERS_START_TIME).do(chargemap_parser)
    while True:
        schedule.run_pending()
