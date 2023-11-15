# Your API KEYS (you need to use your own keys - very long random characters)
from config import MAPBOX_TOKEN, MBTA_API_KEY
import json
import urllib.request
from pprint import pprint

# Useful URLs (you need to add the appropriate parameters for your requests)
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

# A little bit of scaffolding if you want to use it

def build_mapbox_url(query: str) -> str:
    """
    Takes user query to build mapbox api url
    """
    query = query.replace(' ', '%20') # In URL encoding, spaces are typically replaced with "%20"
    return f'{MAPBOX_BASE_URL}/{query}.json?access_token={MAPBOX_TOKEN}&types=poi'

def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.

    Both get_lat_long() and get_nearest_station() might need to use this function.
    """
    with urllib.request.urlopen(url) as f:
        response_text = f.read().decode('utf-8')
        response_data = json.loads(response_text)
    return response_data


def get_lat_long(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/geocoding/ for Mapbox Geocoding API URL formatting requirements.
    """
    mapbox_json = get_json(build_mapbox_url(query=place_name))
    longitude = str((mapbox_json['features'][0]['center'][0]))
    latitude = str((mapbox_json['features'][0]['center'][1]))
    return longitude, latitude



def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
    """
    # latitude = round(latitude, ndigits=5)
    # longitude = round(longitude, ndigits=5)
    url = f"{MBTA_BASE_URL}?api_key={MBTA_API_KEY}&sort=distance&filter%5Blatitude%5D={latitude}&filter%5Blongitude%5D={longitude}"

    response_data = get_json(url)

    station_name = response_data["data"][0]["attributes"]["name"]
    wheelchair_accessible = (
        response_data["data"][0]["attributes"]["wheelchair_boarding"] == 1
    )

    return station_name, wheelchair_accessible


def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.

    This function might use all the functions above.
    # Output: Beacon St opp Walnut St
    """
    longitude, latitude = get_lat_long(place_name)
    station_name, wheelchair_accessible = get_nearest_station(latitude, longitude)
    if wheelchair_accessible: 
        return f"The nearest station to {place_name} is {station_name}. It is wheelchair accessible."
    else:
        return f"The nearest station to {place_name} is {station_name}. It is not wheelchair accessible."
    


def main():
    """
    You should test all the above functions here
    """
    # query = input("Enter place name: ")
    query = 'Harvard'

    print(find_stop_near(place_name=query))


if __name__ == '__main__':
    main()
