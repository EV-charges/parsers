from settings import api_settings
from src.utils.make_request import make_request


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
        # TODO: naming

        places_to_database = make_request(url=api_settings.GET_LIST_ALL_PlACES, params=query_params)
        if places_to_database is not None:
            places = places_to_database.json()['places']

            if not places:
                return places_set

            for place in places:
                inner_ids = [
                    source['inner_id'] for source in place['sources']
                    if source['source'] == source_name
                ]
                # places_set.
                for source in place['sources']:
                    if source['source'] == source_name:
                        inner_id = source['inner_id']
                        places_set.add(inner_id)

        limit += api_settings.NUMBER_RECORDS_IN_ONE_QUERY
        offset += api_settings.NUMBER_RECORDS_IN_ONE_QUERY
