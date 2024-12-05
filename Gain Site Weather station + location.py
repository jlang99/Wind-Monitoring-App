
import requests

def make_stationapi_request(latitude, longitude):
    url = f"https://api.weather.gov/points/{latitude},{longitude}"
    headers = {
        'Content-Type': 'application/ld+json',
    }
    return requests.get(url, headers=headers)

sites = [("Bluebird", '34.6012', '-82.7391')]



for site, lat, long in sites:
    if lat and long:
        response = make_stationapi_request(lat, long)
        if response.status_code == 200:
            data = response.json()
            print(f'{site} | {data}')