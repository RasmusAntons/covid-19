from bin.gmaps import Location
from bin.lib import Covid19Result, UnsupportedLocation
from bin import countries
import os
import pandas as pd
import sys


def who(country: str):
    """
    Returns tuple(avg_cases, cum_cases, avg_deaths, cum_deaths)
    """
    data = pd.read_csv('https://covid19.who.int/WHO-COVID-19-global-data.csv', header=0, index_col=0)
    data = data[data.Country_code == country]

    result = Covid19Result()
    result.region_name = data.Country[0]
    result.avg_cases = sum(cases for cases in data.New_cases.tail(7))/7
    result.cum_cases = data.Cumulative_cases.tail(1)[0]
    result.avg_deaths = sum(cases for cases in data.New_deaths.tail(7))/7
    result.cum_deaths = data.Cumulative_deaths.tail(1)[0]

    return result


def main(address: str, key: str = os.environ.get('API key')):
    location = Location(address, key=key)
    if country_module := countries.impl.get(location.country.lower()):
        try:
            return country_module.lookup(location)
        except UnsupportedLocation:
            pass
    return who(location.country)


if __name__ == '__main__':
    print(main(sys.argv[1] if len(sys.argv) > 1 else 'Manhattan'))
