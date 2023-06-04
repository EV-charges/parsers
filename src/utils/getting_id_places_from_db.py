from settings import ApiSettings
from src.utils.make_request import make_request

api_settings = ApiSettings()


def getting_id_places_from_db(source_name: str) -> set[int]:
    limit = api_settings.NUMBER_RECORDS_IN_ONE_QUERY
    offset = 0
    places_set = set()

    while True:
        query_params = {
            "limit": limit,
            "offset": offset,
            "source": source_name
        }

        places_from_database = make_request(url=api_settings.GET_LIST_ALL_PlACES, params=query_params)
        if places_from_database is not None:
            places = places_from_database.json()['places']

            if not places:
                return places_set

            for place in places:
                inner_ids = [
                    source['inner_id'] for source in place['sources']
                    if source['source'] == source_name
                ]
                places_set.update(inner_ids)

        limit += api_settings.NUMBER_RECORDS_IN_ONE_QUERY
        offset += api_settings.NUMBER_RECORDS_IN_ONE_QUERY
