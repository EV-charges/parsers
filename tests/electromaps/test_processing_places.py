from src.electromaps.run import processing_places


def test_processing_places() -> None:
    res = processing_places(locations_dict=[
        {
            'id': 8272,
            'latitude': 51.507022,
            'longitude': 0.015928,
            'marker': '2.3.3',
            'name': 'London Royal Victoria Docks Tesla Supercharger'
        }]
    )
    assert res == [
        {
            'coordinates': {
                'lat': 51.507022,
                'lng': 0.015928
            },
            'inner_id': 8272,
            'name': 'London Royal Victoria Docks Tesla Supercharger',
            'source': 'electromaps'
        }
    ]
