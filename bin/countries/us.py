from ...bin.lib import classes
import numpy as np
import pandas as pd


def cum2new(cum: np.ndarray):
    new = np.array([0])

    j = 0
    for i in cum:
        new = np.append(new, i - j)
        j = i

    return new[:-1]


def run(region: classes.Region):
    if region.aal2:
        aal = 'counties'
    else:
        aal = 'states'
    url = f'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-{aal}.csv'

    df = pd.read_csv(url)
    df = df[(df.state == region.aal1) & (df.county == region.aal2.split(' ')[0] if region.aal2 else 1)]

    fips = df.fips.head(1).values[0]  # a standard geographic identifier,
    # to make it easier for an analyst to combine this data with other data sets like a map file or population data
    date, cum_cases, cum_deaths = df.date.values, df.cases.values, df.deaths.values

    df = pd.DataFrame(columns=['date', 'new_cases', 'cum_cases', 'new_deaths', 'cum_deaths'])
    df.date, df.cum_cases, df.cum_deaths = date, cum_cases, cum_deaths
    df.new_cases, df.new_deaths = cum2new(cum_cases), cum2new(cum_deaths)

    # -------- population data --------
    state = int(str(fips)[:2])
    county = None
    if region.aal2:
        level, file = 'counties', 'co-est2019-alldata'
        county = int(fips) - 1000*state
    else:
        level, file = 'national', 'nst-est2019-popchg2010_2019'
    url = f'https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/{level}/totals/{file}.csv'

    census = pd.read_csv(url, encoding='ISO-8859-1')
    census = census[(census.STATE == state) & (census.COUNTY == county if county else 1)]
    pop = census.POPESTIMATE2019.head(1).values[0]

    # --------

    data = classes.Covid19Data(df, pop)
    data.source = 'The New York Times'

    return data
