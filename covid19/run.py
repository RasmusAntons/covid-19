from covid19.lib import functions
from covid19 import countries
from covid19 import who
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
        print(data)
        return data


if __name__ == '__main__':
    main('US')