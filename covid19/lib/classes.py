import pandas as pd


def per_mill(pop, num):
    """Returns number per million if population exists."""
    if pop:
        return num * 10**6 / pop
    else:
        return None


class Region:
    """
    """
    def __init__(self, query: str, *args: None, lang: str = 'en'):
        self.query, self.lang = query, lang
        self.cc, self.country, self.aal1, self.aal2, self.aal3, self.local, self.sublocal = \
            (i if i else None for i in args) if args else (None,)*7

    def __repr__(self):
        return f'classes.Region{vars(self)}'


class Covid19Data:
    """
    --------

    date, new_cases, cum_cases, new_deaths, cum_deaths

    yyyy-mm-dd, int, int, int, int

    ...

    yyyy-mm-dd, int, int, int, int

    --------


    """
    def __init__(self, df: pd.DataFrame, pop: int = None):
        self.region = None
        self.source = None
        self.source_url = None

        self.df = df
        self.pop = pop

        def sda(data: pd.core.series.Series):
            return sum(i for i in data.tail(7))/7

        self.sda_cases, self.sda_deaths = sda(df.new_cases), sda(df.new_deaths)
        self.cum_cases, self.cum_deaths = df.cum_cases.tail(1).values[0], df.cum_deaths.tail(1).values[0]
        self.date = df.date.tail(1).values[0]

    @property
    def sda_cpm(self):
        return per_mill(self.pop, self.sda_cases)

    @property
    def sda_dpm(self):
        return per_mill(self.pop, self.sda_deaths)

    @property
    def cum_cpm(self):
        return per_mill(self.pop, self.cum_cases)

    @property
    def cum_dpm(self):
        return per_mill(self.pop, self.cum_cases)

    def __repr__(self):
        return f'classes.Covid19Data{vars(self)}'
