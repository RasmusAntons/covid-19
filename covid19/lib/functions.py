import os
import googlemaps
from covid19.lib import classes


def locate(address: str, lang: str = None, key: str = os.environ.get('API key')):
    """
    Returns classes.Region(cc, aal1, aal2, aal3, local)

    * cc -- Country Code
    * aal -- Administrative Area Level
    * local -- Locality
    """
    gmaps = googlemaps.Client(key=key)

    geocode_result = gmaps.geocode(address=address, language=lang)
    address_components = geocode_result[0]['address_components']

    region = classes.Region(address, lang=lang)

    for component in address_components:
        if 'country' in component['types']:
            region.cc = component['short_name']
            region.country = component['long_name']
        if 'administrative_area_level_1' in component['types']:
            region.aal1 = component['long_name']
        if 'administrative_area_level_2' in component['types']:
            region.aal2 = component['long_name']
        if 'administrative_area_level_3' in component['types']:
            region.aal3 = component['long_name']
        if 'locality' in component['types']:
            region.local = component['long_name']
        if 'sublocality' in component['types']:
            region.sublocal = component['long_name']

    return region
