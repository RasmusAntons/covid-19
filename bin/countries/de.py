from ...bin.lib import classes, functions
import urllib.request
import urllib.parse
import json
import pandas as pd
import datetime
import os


def _query(table, params):
    table = urllib.parse.quote(table)
    params['f'] = 'json'
    query = urllib.parse.urlencode(params)
    url = f'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/{table}/FeatureServer/0/query?{query}'
    with urllib.request.urlopen(url) as r:
        res = json.load(r)
        attrs = [feature['attributes'] for feature in res['features']]
    return attrs


def history_for_state(state_id):
    params = {
        'where': f'IdBundesland=\'{state_id}\'',
        'returnCountOnly': 'false',
        'returnDistinctValues': 'false',
        'orderByFields': 'Meldedatum',
        'groupByFieldsForStatistics': 'Meldedatum',
        'outStatistics': json.dumps([{
            'statisticType': 'sum',
            'onStatisticField': 'AnzahlFall',
            'outStatisticFieldName': 'new_cases'
        }, {
            'statisticType': 'sum',
            'onStatisticField': 'AnzahlTodesfall',
            'outStatisticFieldName': 'new_deaths'
        }, {
            'statisticType': 'sum',
            'onStatisticField': 'SummeFall',
            'outStatisticFieldName': 'cum_cases'
        }, {
            'statisticType': 'sum',
            'onStatisticField': 'SummeTodesfall',
            'outStatisticFieldName': 'cum_deaths'
        }])
    }
    attrs = _query('Covid19_RKI_Sums', params)
    dfs = []
    cols = ('date', 'new_cases', 'cum_cases', 'new_deaths', 'cum_deaths')
    for attr in attrs:
        date = datetime.date.fromtimestamp(attr['Meldedatum'] / 1000)
        new_cases = attr['new_cases']
        cum_cases = attr['cum_cases']
        new_deaths = attr['new_deaths']
        cum_deaths = attr['cum_deaths']
        dfs.append(pd.DataFrame(((date, new_cases, cum_cases, new_deaths, cum_deaths),), columns=cols))
    df = pd.concat(dfs, ignore_index=True)
    return df


def current_by_state(state):
    params = {
        'where': f'LAN_ew_GEN=\'{state}\'',
        'units': 'esriSRUnit_Meter',
        'outFields': 'OBJECTID_1,Fallzahl,Aktualisierung,Death,LAN_ew_EWZ,cases7_bl_per_100k',
        'returnGeometry': 'false'
    }
    attrs = _query('Coronafälle_in_den_Bundesländern', params)
    if len(attrs) == 0:
        raise UnsupportedLocation(f'Invalid state: {state}')
    df = history_for_state(attrs[0]['OBJECTID_1'])
    result = classes.Covid19Data(df, attrs[0]['LAN_ew_EWZ'])
    return result


def history_for_district(district_id):
    params = {
        'where': f'IdLandkreis=\'{district_id}\'',
        'units': 'esriSRUnit_Meter',
        'outFields': 'AnzahlFall,AnzahlTodesfall,SummeFall,SummeTodesfall,Meldedatum',
    }
    attrs = _query('Covid19_RKI_Sums', params)
    dfs = []
    cols = ('date', 'new_cases', 'cum_cases', 'new_deaths', 'cum_deaths')
    for attr in attrs:
        date = datetime.date.fromtimestamp(attr['Meldedatum'] / 1000)
        new_cases = attr['AnzahlFall']
        cum_cases = attr['SummeFall']
        new_deaths = attr['AnzahlTodesfall']
        cum_deaths = attr['SummeTodesfall']
        dfs.append(pd.DataFrame(((date, new_cases, cum_cases, new_deaths, cum_deaths),), columns=cols))
    df = pd.concat(dfs, ignore_index=True)
    return df


def current_by_district(district):
    params = {
        'where': f'GEN=\'{district}\'',
        'units': 'esriSRUnit_Meter',
        'outFields': 'cases,cases_per_100k,cases7_per_100k,deaths,EWZ,RS',
        'returnGeometry': 'false'
    }
    attrs = _query('RKI_Landkreisdaten', params)
    if len(attrs) == 0:
        raise UnsupportedLocation(f'Invalid district: {district}')
    df = history_for_district(attrs[0]['RS'])
    result = classes.Covid19Data(df, attrs[0]['EWZ'])
    return result


def run(region: classes.Region, key: str = os.environ.get('API key')):
    region_de = functions.locate(region.query, lang='de', key=key)
    if region_de.local == 'Berlin':
        if region_de.sublocal:
            region_de.local = f'{region_de.local} {region_de.sublocal}'
        else:
            region_de.local = None
    if region_de.local:
        return current_by_district(region_de.local)
    return current_by_state(region_de.aal1)


class UnsupportedLocation(Exception):
    pass
