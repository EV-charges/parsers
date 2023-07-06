import logging
import time

import schedule

from settings import AllParsersSettings, ElectromapsSettings
from src.utils.getting_id_places_from_db import getting_id_places_from_db
from src.utils.make_request import RequestMethod, make_request
from src.utils.make_request_proxy import make_request_proxy
from src.utils.uploading_db_functions import uploading_comments, uploading_places

settings = ElectromapsSettings()
time_settings = AllParsersSettings()

logger = logging.getLogger(__name__)


def processing_places(
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


def processing_comments(
        places_comments: dict[int, list]
) -> list[dict]:
    result = []

    for place_id, comments in places_comments.items():
        for comment in comments:
            result.append({
                'place_id': place_id,
                'comment_id': comment['idcomment'],
                'author': comment['created_by']['username'],
                'text': comment['comment'],
                'publication_date': comment['created_at'],
                'source': 'electromaps'
            })
    return result


def places_parsing() -> list[dict] | None:
    coordinates = settings.coordinates
    response = make_request_proxy(
        url=settings.PLACES_URL,
        params=coordinates,
        retries_proxy=15,
        method=RequestMethod.GET
    )

    if not response:
        return
    return response.json()


def comments_parsing(headers: dict) -> dict[int, list]:
    places_ids = getting_id_places_from_db(settings.SOURCE_NAME)

    result = {}
    for place_id in places_ids:
        limit = settings.LIMIT
        offset = settings.OFFSET
        place_comments = []

        while True:
            url = settings.PLACES_URL + f'/{place_id}/comments'
            resp = make_request_proxy(
                url=url,
                headers=headers,
                params={
                    'limit': limit,
                    'offset': offset
                },
                retries_proxy=15,
                method=RequestMethod.GET
            )
            if not resp:
                break

            comments = resp.json()
            if not comments:
                break

            place_comments.extend(comments)
            offset += limit

        result[place_id] = place_comments
    return result


def get_access_token() -> dict | str:
    url = settings.URL_GET_TOKEN
    headers = settings.HEADERS_GET_TOKEN
    json = settings.json_get_token
    response = make_request(
        url=url,
        method=RequestMethod.POST,
        headers=headers,
        json=json
    )
    if not response:
        # Временное решение, не до конца понимаю логику, что нам делать, если не получили токен
        return "Can't get token"

    auth_response = response.json()
    access_tokens = auth_response['AuthenticationResult']
    access_token_headers = {
        'X-Em-Oidc-Accesstoken': access_tokens['AccessToken'],
        'X-Em-Oidc-Data': access_tokens['IdToken']
    }
    return access_token_headers


def _electromaps_parser() -> None:
    already_saved_ids = getting_id_places_from_db(settings.SOURCE_NAME)
    logger.info(f'get {len(already_saved_ids)} already saved ids from db')

    places = places_parsing()
    if not places:
        logger.error('Can not get places')

    new_parsing_places = processing_places(places)

    places_added = 0
    for place in new_parsing_places:
        if place['inner_id'] in already_saved_ids:
            continue

        place_add = uploading_places(place)
        if place_add:
            places_added += 1

    logger.info(f'All {places_added} places added in db')

    access_tokens = get_access_token()
    places_comments = comments_parsing(access_tokens)
    comments = processing_comments(places_comments)

    comments_added = 0
    for comment in comments:
        comment_add = uploading_comments(comment)
        if comment_add:
            comments_added += 1

    logger.info(f'All {comments_added} comments added in db')


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
