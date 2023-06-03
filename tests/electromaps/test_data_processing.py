from src.electromaps.run import processing_data


def test_processing_data():
    res = processing_data(locations_dict=[
        {
            'id': 8272,
            'latitude': 51.507022,
            'longitude': 0.015928,
            'marker': '2.3.3',
            'name': 'London Royal Victoria Docks Tesla Supercharger'
        }]
    )
    a = 1
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
