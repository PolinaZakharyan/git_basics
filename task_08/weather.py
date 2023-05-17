#!/usr/bin/env python3

import json
import argparse
import os

def load_wmo_codes():
    import csv
    with open(os.path.join(os.path.dirname(__file__), 'wmo_codes.csv')) as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        return [row[1].strip()[1:-1] for row in reader]

WMO_CODES = load_wmo_codes()

def make_argparser():
    parser = argparse.ArgumentParser(
        prog='weather',
        description='request weather for the given city or the coordinates',
        epilog='Text at the bottom of help'
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('city', nargs='?', type=str,
        help='format: "city" or "country/city"')

    group.add_argument('--coords', '-c', nargs=2, type=float,
        metavar="N", help="latitude longitude")

    return parser

from urllib import request

def make_request(url):
    """Issue GET request to URL returning text."""
    respfile = request.urlopen(url)

    hdr = respfile.headers
    ct = hdr.get('content-type', '; charset=UTF-8')
    enc = ct.split(';')[-1].split('=')[-1]
    enc = enc.lower()

    bindata = respfile.read()
    data = bindata.decode(encoding=enc)
    return data


class WeatherError(Exception):
    pass


class CityNotFoundError(WeatherError, LookupError):
    """Raised when city not found."""
    pass


class RequestData:
    URL_TEMPLATE = ''

    def request(self, **kwargs):
        """Make request to remote URL parsing json result."""
        # Create url for further GET request to OpenMeteo
        url = self.URL_TEMPLATE.format(**kwargs)

        text = make_request(url=url)
        data = json.loads(text)
        return data


class City(RequestData):
    URL_TEMPLATE = (
        'https://geocoding-api.open-meteo.com/v1/search?name={name}&country={country}')

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

    def request(self):
        cities = self.find_cities()

        if self.name not in cities:
            raise CityNotFoundError(self.name)

        for k, v in cities[self.name].items():
            setattr(self, k, v)

    def find_cities(self):
        data = super().request(name=self.name, country=self.country)
        data = data.get('results', {})

        extract = ['latitude', 'longitude', 'country']
        res = {entry['name']: {k: entry[k] for k in extract} for entry in data}
        return res


class Weather(RequestData):
    URL_TEMPLATE = ('https://api.open-meteo.com/v1/forecast?'
                    'latitude={lat}&longitude={lon}&current_weather=true')

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
            raise WeatherError(msg)

        self.requested_object = city.name if city else f"{latitude}, {longitude}"
        self.lat = latitude
        self.lon = longitude
        self.data = None

    def __repr__(self):
        n = type(self).__name__
        return f'{n}(latitude={self.lat}, longitude={self.lon})'

    def request(self):
        data = super().request(lat=self.lat, lon=self.lon)
        self.data = data

    @property
    def temperature(self):
        """Retreive temperature from OpenMeteo response."""
        if self.data is None:
            self.request()
        return self.data['current_weather']['temperature']

    @property
    def weather(self):
        """Retreive weather description from OpenMeteo response."""
        if self.data is None:
            self.request()
        code = self.data['current_weather']['weathercode']
        if code >= len(WMO_CODES):
            return "unknown"
        return WMO_CODES[code]

    @property
    def windspeed(self):
        """Retreive windspeed from OpenMeteo response."""
        if self.data is None:
            self.request()
        return self.data['current_weather']['windspeed']

    @property
    def winddirection(self):
        """Retreive winddirection from OpenMeteo response."""
        if self.data is None:
            self.request()
        return self.data['current_weather']['winddirection']

    @property
    def time(self):
        """Retreive time from OpenMeteo response."""
        if self.data is None:
            self.request()
        return self.data['current_weather']['time']

if __name__ == '__main__':

    from sys import argv
    parser = make_argparser()

    ns = parser.parse_args(argv[1:])

    city, lat, long = ns.city, None, None
    if ns.coords:
        lat, long = ns.coords[0], ns.coords[1]

    wth = Weather(city, lat, long)

    resp = f'Weather in {wth.requested_object}:\n'
    resp += f' time:          {wth.time}\n'
    resp += f' temperature:   {wth.temperature}\n'
    resp += f' windspeed:     {wth.windspeed}\n'
    resp += f' winddirection: {wth.winddirection}\n'
    resp += f' weather:       {wth.weather}\n'

    print(resp)
