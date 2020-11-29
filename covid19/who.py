from covid19.lib import classes
import pandas as pd


def run(region: classes.Region):
    url = 'https://covid19.who.int/WHO-COVID-19-global-data.csv'

    df = pd.read_csv(url)
    df = df[df.Country_code == region.cc]

    date, new_cases, cum_cases, new_deaths, cum_deaths = \
        df.Date_reported.values, \
        df.New_cases.values, df.Cumulative_cases.values, df.New_deaths.values, df.Cumulative_deaths.values

    df = pd.DataFrame(columns=['date', 'new_cases', 'cum_cases', 'new_deaths', 'cum_deaths'])
    df.date, df.new_cases, df.cum_cases, df.new_deaths, df.cum_deaths = \
        date, new_cases, cum_cases, new_deaths, cum_deaths

    un = pd.read_csv('WPP2019_TotalPopulation.csv')
    if region.cc == 'US':
        region.country = 'United States of America'
    # add failed country population exceptions here
    un = un[un.Location == region.country]
    pop = un.PopTotal.head(1).values[0]*1000

    data = classes.Covid19Data(df, pop)
    data.source = 'WHO'
    data.source_url = 'https://covid19.who.int/'
    data.region = region.country

    return data