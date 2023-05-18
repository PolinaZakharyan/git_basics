#!/usr/bin/env python3

import logging
import json
import argparse
import os
import sys
from time import sleep

from exceptlogger import exceptlogger

DEFAULT_MONTORNG_PERIOD = 10

logging.basicConfig(filename='weather.log', filemode='a')
LOGGER = logging.getLogger(__name__)

# convert our log level to lib level
LOG_LVL = {
    0: 'CRITICAL',
    1: 'ERROR',
    2: 'WARNING',
    3: 'INFO',
    4: 'DEBUG'
}

@exceptlogger()
def load_wmo_codes():
    import csv
    with open(os.path.join(os.path.dirname(__file__), 'wmo_codes.csv')) as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        return [row[1].strip()[1:-1] for row in reader]

WMO_CODES = load_wmo_codes()

@exceptlogger()
def make_argparser():
    parser = argparse.ArgumentParser(
        prog='weather',
        description='request weather for the given city or the coordinates'
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('city', nargs='?', type=str,
        help='Location, format: "city" or "country/city"')

    group.add_argument('--coords', '-c', nargs=2, type=float,
        metavar="N", help="Latitude and longitude")

    parser.add_argument('--monitor', '-m', nargs='?', type=argparse.FileType('w'), const=sys.stdout,
        metavar="FILE", help='Monitoring log file, default is std out')

    parser.add_argument('--period', nargs='?', type=int,
        metavar="N", help=f"Monitoring period in seconds, default is {DEFAULT_MONTORNG_PERIOD}")

    parser.add_argument('--verbose', '-v', action='count', default=0)

    return parser

class WeatherAPIError(Exception):
    pass


class CityNotFoundError(WeatherAPIError, LookupError):
    """Raised when city not found."""
    pass


from urllib import request

@exceptlogger()
def make_request(url):
    """Issue GET request to URL returning text."""
    LOGGER.info('make_request call with url = %s', url)
    try:
        respfile = request.urlopen(url)
    except Exception as e:
        raise WeatherAPIError(e.args)

    hdr = respfile.headers
    ct = hdr.get('content-type', '; charset=UTF-8')
    enc = ct.split(';')[-1].split('=')[-1]
    enc = enc.lower()

    bindata = respfile.read()
    data = bindata.decode(encoding=enc)
    return data


class RequestData:
    URL_TEMPLATE = ''

    @exceptlogger()
    def request(self, **kwargs):
        """Make request to remote URL parsing json result."""
        # Create url for further GET request to OpenMeteo
        url = self.URL_TEMPLATE.format(**kwargs)

        text = make_request(url=url)

        try:
            data = json.loads(text)
        except Exception as e:
            raise WeatherAPIError(e.args)
        return data


class City(RequestData):
    URL_TEMPLATE = (
        'https://geocoding-api.open-meteo.com/v1/search?name={name}&country={country}')

    @exceptlogger()
    def __init__(self, name=None, latitude=None, longitude=None):

        if name is not None:
            name = name.title()

        country = None
        if '/' in name:
            country, name = name.split('/')

        self.country = country
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

        LOGGER.debug('City initialized with \
            country, name, latitude, longitude = %s',
            str([country, name, latitude, longitude])
        )

    @exceptlogger()
    def request(self):
        cities = self.find_cities()

        if self.name not in cities:
            raise CityNotFoundError(self.name)

        for k, v in cities[self.name].items():
            setattr(self, k, v)

    @exceptlogger()
    def find_cities(self):
        data = super().request(name=self.name, country=self.country)
        data = data.get('results', {})

        extract = ['latitude', 'longitude', 'country']
        res = {entry['name']: {k: entry[k] for k in extract} for entry in data}
        return res


class Weather(RequestData):
    URL_TEMPLATE = ('https://api.open-meteo.com/v1/forecast?'
                    'latitude={lat}&longitude={lon}&current_weather=true')

    @exceptlogger()
    def __init__(self, city=None, latitude=None, longitude=None):

        if isinstance(city, str):
            city = City(city)

        if isinstance(city, City):
            if (city.latitude is None or city.longitude is None):
                city.request()
            latitude = city.latitude
            longitude = city.longitude

        if latitude is None or longitude is None:
            msg = ('Either a valid city or a pair of latitude, '
                   'longitude must be provided')
            raise WeatherAPIError(msg)

        requested_object = city.name if city else f"{latitude}, {longitude}"

        self.requested_object = requested_object
        self.lat = latitude
        self.lon = longitude
        self.data = None

        LOGGER.debug('Weather initialized with \
            requested_object, latitude, longitude = %s',
            str([requested_object, latitude, longitude])
        )

    @exceptlogger()
    def __repr__(self):
        n = type(self).__name__
        return f'{n}(latitude={self.lat}, longitude={self.lon})'

    @exceptlogger()
    def request(self):
        data = super().request(lat=self.lat, lon=self.lon)
        self.data = data

    @property
    def temperature(self):
        """Retreive temperature from OpenMeteo response."""
        with exceptlogger('Weather.temperature'):
            if self.data is None:
                self.request()
            return self.data['current_weather']['temperature']

    @property
    def weather(self):
        """Retreive weather description from OpenMeteo response."""
        with exceptlogger('Weather.weather'):
            if self.data is None:
                self.request()
            code = self.data['current_weather']['weathercode']
            if code >= len(WMO_CODES):
                return "unknown"
            return WMO_CODES[code]

    @property
    def windspeed(self):
        """Retreive windspeed from OpenMeteo response."""
        with exceptlogger('Weather.windspeed'):
            if self.data is None:
                self.request()
            return self.data['current_weather']['windspeed']

    @property
    def winddirection(self):
        """Retreive winddirection from OpenMeteo response."""
        with exceptlogger('Weather.winddirection'):
            if self.data is None:
                self.request()
            return self.data['current_weather']['winddirection']

    @property
    def time(self):
        """Retreive time from OpenMeteo response."""
        with exceptlogger('Weather.time'):
            if self.data is None:
                self.request()
            return self.data['current_weather']['time']

    @property
    def dump(self) -> str:
        self.request()
        resp = f'Weather in {wth.requested_object}:\n'
        resp += f' time:          {wth.time}\n'
        resp += f' temperature:   {wth.temperature}\n'
        resp += f' windspeed:     {wth.windspeed}\n'
        resp += f' winddirection: {wth.winddirection}\n'
        resp += f' weather:       {wth.weather}\n'
        return resp

if __name__ == '__main__':

    from sys import argv
    parser = make_argparser()

    ns = parser.parse_args(argv[1:])

    if __debug__:
        logging.basicConfig(stream=sys.stdout)

    LOGGER.setLevel(LOG_LVL.get(ns.verbose, 'DEBUG'))
    LOGGER.debug('weather call with args = %s', str(ns))

    monitor, period = ns.monitor, ns.period
    if (period is not None) and (monitor is None):
        raise RuntimeError('--monitor option shall be provided explicitly if period is specified')


    city, lat, long = ns.city, None, None
    if ns.coords:
        lat, long = ns.coords[0], ns.coords[1]

    wth = Weather(city, lat, long)

    if monitor:
        if not period:
            period = DEFAULT_MONTORNG_PERIOD
            LOGGER.warning('period option not set, using default value %d',
                DEFAULT_MONTORNG_PERIOD)

        while True:
            with exceptlogger('monitoring loop'):
                monitor.write(str(wth.temperature) + "\n")
                monitor.flush()
            sleep(period)

    else:
        print(wth.dump)
