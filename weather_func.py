from pyowm import OWM
from pyowm.commons.exceptions import NotFoundError
WEATHER_API = OWM('')


def input_error(func):
    """Important exception — it needs for catch incorrect city.
        Should add this except at the main input_error func"""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFoundError:
            return 'Unknown city, please try again.'
    return inner


@input_error
def get_weather(args: list):
    """Function shows the weather in the city selected by the user. If entered incorrectly, a NotFoundError occurs. """
    city = args  # city = args[0].capitalize()
    manager = WEATHER_API.weather_manager()
    observe = manager.weather_at_place(city)
    country = observe.to_dict()['location']['country']
    if country == "RU":
        return "WE NOT WORKS WITH TERRORISTS! Enter the city again."
    else:
        w = observe.weather
        temp = w.temperature('celsius')

    return f"""
    Weather in {city}.
    Temperature is {temp['temp']} C.
    Feels like: {temp['feels_like']} C.
    Status: {w.status} 
    """

