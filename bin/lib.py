class Covid19Result:
    def __init__(self):
        self.region_name = self.population = None
        self.avg_cases = self.cum_cases = self.avg_deaths = self.cum_deaths = None

    def __str__(self):
        return str(vars(self))


class UnsupportedLocation(Exception):
    pass
