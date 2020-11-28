from ..bin.lib import classes
from ..bin.lib import functions
from ..bin import countries
import pandas as pd
import os


def main(address, key: str = os.environ.get('API key')):
    region = functions.locate(address=address, key=key)
    print(region)
    if region.aal1 and region.cc in countries.countries:
        if region.cc == 'US':
            data = countries.us.run(region)
            return data
        elif region.cc == 'DE':
            data = countries.de.run(region, key=key)
            return data
    else:
        # TODO: write who.py
        return 0
