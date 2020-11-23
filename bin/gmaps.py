import os
import googlemaps


def locate(key: str = os.environ.get('API key'), address: str = None):
    """
    A google API key is required to use this function. By default, it's defined as an environmental variable 'API key'.

    Address is a location that is acceptable by google. They can range from cities to countries.

    Returned is a tuple(country, aal1, aal2, aal3, locality, sublocality) where aal is administrative area level.
    """
    gmaps = googlemaps.Client(key=key)

    geocode_result = gmaps.geocode(address=address)
    address_components = geocode_result[0]['address_components']

    country, aal1, aal2, aal3, locality, sublocality = (None,)*6

    for component in address_components:
        if 'country' in component['types']:
            country = component['long_name']
        if 'administrative_area_level_1' in component['types']:
            aal1 = component['long_name']
        if 'administrative_area_level_2' in component['types']:
            aal2 = component['long_name']
        if 'administrative_area_level_3' in component['types']:
            aal3 = component['long_name']
        if 'locality' in component['types']:
            locality = component['long_name']
        if 'sublocality' in component['types']:
            sublocality = component['long_name']

    return country, aal1, aal2, aal3, locality, sublocality


if __name__ == '__main__':
    print(locate(address='Manhattan'))
