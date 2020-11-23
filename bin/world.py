from bin import gmaps
from bin import countries
import os
import pandas as pd


def who(country: str):
    data = pd.read_csv('https://covid19.who.int/WHO-COVID-19-global-data.csv', header=0, index_col=0)
    data = data[data.Country_code == country]

    avg_cases = sum(cases for cases in data.New_cases.tail(7))/7
    cum_cases = data.Cumulative_cases.tail(1)[0]
    avg_deaths = sum(cases for cases in data.New_deaths.tail(7))/7
    cum_deaths = data.Cumulative_deaths.tail(1)[0]

    return avg_cases, cum_cases, avg_deaths, cum_deaths


def main(address: str, key: str = os.environ.get('API key')):
    address = gmaps.locate(address=address)

    # TODO: make it so that if the country in address is a country in the folder /countries, it performs the script
    #  relevant to that country rather than from the world.
    # if country in countries:
    #     return country...
    # else:
    #     return who(address[0])

    return who(address[0])


if __name__ == '__main__':
    print(main('Manhattan'))
