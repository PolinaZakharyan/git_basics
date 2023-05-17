from weather import *

DEFAULT_CITY = 'kyiv'

def test_init_weather_with_coords():
    city = City(DEFAULT_CITY)
    city.request()

    wth = Weather(latitude=city.latitude, longitude=city.longitude)
    wth.request()

    assert wth.data is not None
    assert wth.temperature is not None
    print('test_init_weather_with_coords passed')


def test_init_weather_with_cityname(name=DEFAULT_CITY):

    wth = Weather(city=name)
    wth.request()

    assert wth.data is not None
    assert wth.temperature is not None
    print('test_init_weather_with_cityname passed with name = %s' % name)

def test_init_weather_with_cityobj():

    wth = Weather(city=City(DEFAULT_CITY))
    wth.request()

    assert wth.data is not None
    assert wth.temperature is not None
    print('test_init_weather_with_cityobj passed')


if __name__ == '__main__':
    test_init_weather_with_coords()
    test_init_weather_with_cityname('kyiv')
    test_init_weather_with_cityname('Kryzhopil')
    test_init_weather_with_cityname('Ukraine/Kyiv')
    test_init_weather_with_cityobj()