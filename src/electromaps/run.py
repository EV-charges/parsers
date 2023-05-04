import requests


def run() -> None:
    pass


def get_data(url):
    req = requests.get(url, headers=headers)
    return req.json()


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0 (Edition Yx 05)",
    "Referer": "https://map.electromaps.com/"
}
url = f'https://www.electromaps.com/mapi/v2/locations?latNE=51.77429497247951&lngNE=0.321869842498387&latSW=50.96494968728243&lngSW=-1.6614686519200745&realtime=false&connectors=&types=ON_STREET,PARKING,AIRPORT,CAMPING,HOTEL,RESTAURANT,SHOP,WORKSHOP,FUEL_STATION,CAR_DEALER,MALL,TAXI&power=3&skipAuthTokenValidation=true'

locations_dict = (get_data(url))
for location in locations_dict:
    id = location['id']
    name = location['name']
    latitude = location['latitude']
    longitude = location['longitude']
    print(id, name, latitude, longitude)