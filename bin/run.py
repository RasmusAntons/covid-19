from ..bin.lib import functions
from ..bin import countries
from ..bin import who
import os


def main(address, key: str = os.environ.get('API key')):
    region = functions.locate(address=address, key=key)

    if region.aal1 and region.cc in countries.countries:
        if region.cc == 'US':
            data = countries.us.run(region)
            return data
        elif region.cc == 'DE':
            data = countries.de.run(region, key=key)
            return data
    else:
        data = who.run(region)
        return data
