import pytest

from src.chargemap.run import data_processing


def test_data_processing_count_zero() -> None:
    result = data_processing({'count': 0})
    assert result is None


@pytest.mark.parametrize('response', [{"count": 1, "items": [{"type": "cluster"}]},
                                      {"count": 1, "items": [{"type": "pool"}]}
                                      ])
def test_data_processing_key_exception(response: dict) -> None:
    with pytest.raises(KeyError):
        data_processing(response)


def test_data_processing_correct_return(chargemap_json: dict) -> None:
    result = data_processing(chargemap_json)
    assert result == [{"id": 218379,
                       "lat": 51.4252777,
                       "lng": 0.099236,
                       "city": "London",
                       "street": "Cray Road",
                       "name": "daniel evans"
                       }]
