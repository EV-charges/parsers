import json
from pathlib import Path

import pytest

from settings import BASE_DIR

PLACES_JSON = Path(BASE_DIR, 'tests', 'data', 'chargemap_places.json')

@pytest.fixture()
def chargemap_places_json() -> dict:
    with open(PLACES_JSON) as file:
        result = json.load(file)
    return result
