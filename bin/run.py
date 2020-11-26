from bin.lib import classes
from bin.lib import functions
from bin import countries
import pandas as pd


def main(address):
    region = functions.locate(address=address)

    if region.aal1 and region.cc in countries.countries:
        if region.cc == 'US':
            data = countries.us.run(region)
            return data
        elif region.cc == 'DE':
            data = countries.de.run(region)
            return data
    else:
        # TODO: write who.py
        return 0
