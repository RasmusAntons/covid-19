import os
import googlemaps
from sqlitedict import SqliteDict


class Location:
    def __init__(self, address: str, key: str = os.environ.get('API key'), language=None):
        self.country = self.aal1 = self.aal2 = self.aal3 = self.locality = self.sublocality = None
        self.query = address
        self.key = key
        gmaps = googlemaps.Client(key=key)
        cache_file = './gmaps_cache.sqlite' if language is None else f'./gmaps_cache_{language}.sqlite'
        with SqliteDict(cache_file) as cache:
            self.geocode_result = cache.get(address)
        if self.geocode_result is None:
            self.geocode_result = gmaps.geocode(address, language=language)
            with SqliteDict(cache_file) as cache:
                cache[address] = self.geocode_result
                cache.commit()
        if not self.geocode_result:
            raise ValueError(f'Invalid location: {address}')
        address_components = self.geocode_result[0]['address_components']
        for component in address_components:
            if 'country' in component['types']:
                self.country = component['short_name']
            if 'administrative_area_level_1' in component['types']:
                self.aal1 = component['long_name']
            if 'administrative_area_level_2' in component['types']:
                self.aal2 = component['long_name']
            if 'administrative_area_level_3' in component['types']:
                self.aal3 = component['long_name']
            if 'locality' in component['types']:
                self.locality = component['long_name']
            if 'sublocality' in component['types']:
                self.sublocality = component['long_name']

    def __str__(self):
        return str(self.geocode_result)
