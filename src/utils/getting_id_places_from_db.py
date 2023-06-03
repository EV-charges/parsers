from settings import ApiSettings
from src.utils.make_request import make_request

api_settings = ApiSettings()


# def get_places_ids_from_db()
def getting_id_places_from_db(source_name: str) -> set[int]:
    limit = api_settings.NUMBER_RECORDS_IN_ONE_QUERY
    offset = 0
    places_ids = set()

    while True:
        query_params = {
            "limit": limit,
            "offset": offset,
            "source": source_name
        }

        response = make_request(
            url=api_settings.GET_LIST_ALL_PlACES, params=query_params
        )
        if not response:
            return places_ids

        places = response.json()['places']
        if not places:
            return places_ids

        for place in places:
            for source in place['sources']:
                if source['source'] == source_name:
                    inner_id = source['inner_id']
                    places_ids.add(inner_id)

        limit += api_settings.NUMBER_RECORDS_IN_ONE_QUERY
        offset += api_settings.NUMBER_RECORDS_IN_ONE_QUERY
