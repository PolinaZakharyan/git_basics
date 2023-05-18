import pytest
from weather import *

TEST_CITIES = ['kyiv', 'Kryzhopil', 'Ukraine/Kyiv', 'Lol', 'Kek']


@pytest.mark.parametrize('name', TEST_CITIES)
def test_city_init_and_repr(name):
    assert City(name).__repr__()

@pytest.mark.parametrize('name', TEST_CITIES)
def test_init_weather_with_cityname(name):

    wth = Weather(city=name)
    wth.request()

    assert wth.data is not None
    assert wth.temperature is not None
    print('test_init_weather_with_cityname passed with name = %s' % name)

@pytest.mark.parametrize('name', ['111', '222', 'no-such-sity'])
def test_error_init_weather(name):
    try:
        Weather(city=name)
        assert False, "should fail" # pragma: no cover
    except CityNotFoundError:
        pass
    except: # pragma: no cover
        assert False, "unknown exception"

@pytest.mark.parametrize('coords', [(0, 0), (1,1), (1.5, 100.5)])
def test_init_weather_with_coords(coords):
    assert Weather(latitude=coords[0], longitude=coords[1]).dump

def test_init_weather_with_cityobj():

    wth = Weather(city=City('kyiv'))
    wth.request()

    assert wth.data is not None
    assert wth.temperature is not None
    assert repr(wth)
    print('test_init_weather_with_cityobj passed')

def test_parser():
    assert make_argparser()
