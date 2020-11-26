from bin.lib import classes
from bin.lib import functions
from bin import countries
import pandas as pd


def main(address):
    region = classes.Region('US', 'New Jersey', None, None, 'Paterson')  # functions.locate(address=address)

    if region.aal1 and region.cc in countries.countries:
        if region.cc == 'US':
            data = countries.us.run(region)
            return data
    else:
        print('you gotta do WHO')


if __name__ == '__main__':
    print(
        main(
            address='paterson nj'
        )
    )