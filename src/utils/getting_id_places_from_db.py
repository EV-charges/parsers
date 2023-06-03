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

        places_to_database = make_request(url=api_settings.GET_LIST_ALL_PlACES, params=query_params)
        if places_to_database is not None:
            data = places_to_database.json()['places']
        if data:
            for place in data:
                for source in place['sources']:
                    if source['source'] == source_name:
                        inner_id = source['inner_id']
                        places_set.add(inner_id)
        else:
            return places_set

        limit += api_settings.NUMBER_RECORDS_IN_ONE_QUERY
        offset += api_settings.NUMBER_RECORDS_IN_ONE_QUERY
