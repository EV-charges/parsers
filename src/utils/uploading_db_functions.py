import requests

from settings import api_settings
from src.utils.make_request import RequestMethod, make_request


def uploading_places(place: dict) -> requests.Response | None:
    r = make_request(
        url=api_settings.get_or_post_places_url,
        json=place,
        method=RequestMethod.POST,
        allow_status_codes=(409,)
    )
    return r


def uploading_comments(comment: dict) -> requests.Response | None:
    r = make_request(
        url=api_settings.post_comments_url,
        json=comment,
        method=RequestMethod.POST,
        allow_status_codes=(409,)
    )
    return r
