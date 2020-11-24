from bin.gmaps import Location
from bin.lib import Covid19Result, UnsupportedLocation
import urllib.request
import urllib.parse
import json


def current_by_district(district):
    url = 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/RKI_Landkreisdaten/FeatureServer/0/query'
    params = {
        'where': f'GEN=\'{district}\'',
        'units': 'esriSRUnit_Meter',
        'outFields': 'cases,cases_per_100k,cases7_per_100k,deaths',
        'returnGeometry': 'false',
        'f': 'json',
    }
    query = f'{url}?{urllib.parse.urlencode(params)}'
    with urllib.request.urlopen(query) as r:
        res = json.load(r)
        if len(res['features']) == 0:
            raise ValueError('Invalid district')
        attr = res['features'][0]['attributes']
    result = Covid19Result()
    result.region_name = district
    result.population = attr['cases'] / attr['cases_per_100k']
    result.avg_cases = attr['cases7_per_100k'] * result.population / 7
    result.cum_cases = attr['cases']
    result.cum_deaths = attr['deaths']
    return result


def lookup(location: Location):
    loc_de = Location(location.query, key=location.key, language='de')
    for district in [f'{loc_de.locality} {loc_de.sublocality}', loc_de.locality]:
        try:
            return current_by_district(district)
        except ValueError:
            pass
    else:
        raise UnsupportedLocation(f'Location not found: {loc_de.locality} ({loc_de.sublocality})')
