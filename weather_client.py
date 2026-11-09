import requests

API_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherAPIError(Exception):
    """Eget fel som till när API-anropet misslyckas."""


def fetch_weather(latitude, longitude):
    """Hämtar väderdata från Open-Meteo för koordinater."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": 3,
    }

    try:
        # Skickar GET-anrop med 5 sekunders timeout
        response = requests.get(API_URL, params=params, timeout=5)
        # Kontrollerar att statuskoden är OK (annars kastas HTTPError)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        # Fångar alla fel från requests (t.ex. timeout eller 404/500)
        # och kastar vårt eget fel med ett tydligt meddelande
        raise WeatherAPIError(
            "Kunde inte hämta väderdata från API:et just nu."
        ) from error
