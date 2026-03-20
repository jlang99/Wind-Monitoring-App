
import requests

def make_stationapi_request(latitude, longitude):
    url = f"https://api.weather.gov/points/{latitude},{longitude}"
    headers = {
        'Content-Type': 'application/ld+json',
    }
    return requests.get(url, headers=headers)

sites = {("Wellons", '35.510813', '-78.292403')}



for site, lat, long in sites:
    if lat and long:
        response = make_stationapi_request(lat, long)
        if response.status_code == 200:
            data = response.json()
            gridId = data.get('properties', {}).get('gridId')
            gridX = data.get('properties', {}).get('gridX')
            gridY = data.get('properties', {}).get('gridY')

            print(f'{site} | Grid ID: {gridId}, Grid X: {gridX}, Grid Y: {gridY}')