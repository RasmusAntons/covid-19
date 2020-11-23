from bin import gmaps
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

    avg_cases = sum(cases for cases in data.New_cases.tail(7))/7
    cum_cases = data.Cumulative_cases.tail(1)[0]
    avg_deaths = sum(cases for cases in data.New_deaths.tail(7))/7
    cum_deaths = data.Cumulative_deaths.tail(1)[0]

    return avg_cases, cum_cases, avg_deaths, cum_deaths


def main(address: str, key: str = os.environ.get('API key')):
    country, aal1, aal2, aal3, locality, sublocality = gmaps.locate(address=address, key=key)

    # TODO: make it so that if the country in address is a country in the folder /countries, it performs the script
    #  relevant to that country rather than from the world.
    if country_module := countries.impl.get(country.lower()):
        return country_module.lookup(country, aal1, aal2, aal3, locality, sublocality)
    else:
        return who(country)


if __name__ == '__main__':
    print(main(sys.argv[1] if len(sys.argv) > 1 else 'Manhattan'))
