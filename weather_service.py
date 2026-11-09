# 5 städerna och koordinater
CITIES = {
    "Stockholm": {"latitude": 59.33, "longitude": 18.07},
    "Göteborg": {"latitude": 57.71, "longitude": 11.97},
    "Malmö": {"latitude": 55.61, "longitude": 13.00},
    "Umeå": {"latitude": 63.83, "longitude": 20.26},
    "Kiruna": {"latitude": 67.86, "longitude": 20.23},
}


def is_valid_city(city):
    """Kollar om en stad finns med i listan över tillåtna städer."""
    return city in CITIES


def get_coordinates(city):
    """Hämtar latitud och longitud för en stad, eller None om staden saknas."""
    return CITIES.get(city)
