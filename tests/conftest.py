import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from settings import BASE_DIR

PLACES_JSON = Path(BASE_DIR, 'tests', 'data', 'chargemap_places.json')


@pytest.fixture()
def chargemap_places_json() -> dict:
    with Path.open(PLACES_JSON) as file:
        result = json.load(file)
    return result


@pytest.fixture
def mock_make_request() -> Mock:
    with patch('src.utils.make_request.make_request') as mock:
        yield mock


@pytest.fixture()
def set_id() -> set[int]:
    return {1, 2, 3}
