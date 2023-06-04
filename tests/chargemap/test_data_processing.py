from unittest.mock import Mock

import pytest

from src.chargemap.run import data_processing_and_save_db


def test_data_processing_count_zero(set_id: set[int]) -> None:
    result = data_processing_and_save_db({'count': 0}, set_id)
    assert result == 0


def test_data_processing_logging_cluster(set_id: set[int]) -> None:
    response = {"count": 1, "items": [{"type": "cluster", "lat": 1, "lng": 2}]}
    result = data_processing_and_save_db(response, set_id)
    assert result == 0


def test_data_processing_error_wrong_key(set_id: set[int]) -> None:
    response = {"count": 1, "items": [{"type": "pool"}]}
    with pytest.raises(KeyError):
        data_processing_and_save_db(response, set_id)


def test_data_processing_correct_return(mock_make_request: Mock, chargemap_places_json: dict, set_id: set[int]) -> None:
    mock_make_request.return_value = True
    result = data_processing_and_save_db(chargemap_places_json, set_id)
    assert result == 1
