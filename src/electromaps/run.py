import json
from settings import ElectromapsSettings, ApiSettings
from src.utils.make_request import make_request, RequestMethod

settings = ElectromapsSettings()
api_settings = ApiSettings()


def processing_data(locations_dict: dict) -> list[dict[str, int | str | float]]:
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
    return result


def electromaps_parser() -> list[dict[str, int | str | float]]:
    coordinates = settings.coordinates
    response = make_request(url=settings.PLACES_URL + coordinates)
    return processing_data(response.json())


def record_new_places() -> None:
    places_from_db = make_request(url=api_settings.GET_LIST_ALL_PlACES + settings.SOURCE_NAME).json()
    already_saved_id = set()

    for place in places_from_db['places']:
        for source in place['sources']:
            if source['source'] == settings.SOURCE_NAME:
                inner_id = source['inner_id']
                already_saved_id.add(inner_id)

    new_parsing_places = electromaps_parser()
    for place in new_parsing_places:
        if place['inner_id'] not in already_saved_id:
            place_json = json.dumps(place)
            make_request(url=api_settings.POST_PLACES, data=place_json, method=RequestMethod.POST)


def run() -> None:
    record_new_places()


