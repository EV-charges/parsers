import json

import pytest


@pytest.fixture()
def chargemap_json() -> dict:
    with open('tests/data/chargemap_places.json') as file:
        result = json.load(file)
    return result
