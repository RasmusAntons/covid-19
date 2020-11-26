from bin.lib import classes
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
    date, cum_cases, cum_deaths = df.date.values, df.cases.values, df.deaths.values
    df = pd.DataFrame(columns=['date', 'new_cases', 'cum_cases', 'new_deaths', 'cum_deaths'])
    df.date, df.cum_cases, df.cum_deaths = date, cum_cases, cum_deaths
    df.new_cases, df.new_deaths = cum2new(cum_cases), cum2new(cum_deaths)

    data = classes.Covid19Data(df)

    return data
