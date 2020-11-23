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
    pop = attr['cases'] / attr['cases_per_100k']
    return attr['cases7_per_100k'] * pop / 7, attr['cases'], None, attr['deaths']


def lookup(country, aal1, aal2, aal3, locality, sublocality):
    for district in [f'{locality} {sublocality}', locality]:
        try:
            return current_by_district(district)
        except ValueError:
            pass
    else:
        raise ValueError('Location not found')
