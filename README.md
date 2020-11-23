# covid-19
## Description
COVID-19 World Data

Want to know the recent 7 day average and cumulative data for COVID-19 cases and deaths for a given location?
Whatever this thingy is can give you just that.
## Requirements
* Python 3.5 or later.
* pandas

    `pip install pandas`
* googlemaps

    `pip install googlemaps`
    * A Google Maps API key.
## Usage
I'm terrible at organizing code before I write it, so currently, the main module is `world.py`.

As it stands at the moment, the only locational data that's used is the world data from the [WHO](https://covid19.who.int/).

Here's a quick example:
```python
from covid-19.bin import world

# Returns tuple(avg_cases, cum_cases, avg_deaths, cum_deaths)
world.main(address='Manhattan, NY', key='Add Your Key here')
```
>`(168017.7142857143, 11972556, 1453.2857142857142, 253931)` as of 2020-11-23
>
>This is also just the country level data, cause I didn't add anything more specific yet :weary:
