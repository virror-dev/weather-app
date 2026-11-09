import pandas as pd
import plotly.express as px

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
    """Hämtar koordinater för en stad, eller None om staden saknas."""
    return CITIES.get(city)


def parse_current_weather(data):
    """Plockar ut nuvarande temperatur och vindstyrka ur API-svaret."""
    if not data or "current" not in data:
        raise ValueError("Saknar data för nuvarande väder.")

    current = data["current"]
    if "temperature_2m" not in current or "wind_speed_10m" not in current:
        raise ValueError("Ofullständig data för nuvarande väder.")

    return {
        "temperature": current["temperature_2m"],
        "wind_speed": current["wind_speed_10m"],
    }


def parse_daily_forecast(data):
    """Gör om API-svaret till en lista med dagar."""
    if not data or "daily" not in data:
        raise ValueError("Saknar prognosdata.")

    daily = data["daily"]
    required_keys = [
        "time",
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
    ]

    # Kontrollera att alla listor finns med och inte är tomma
    for key in required_keys:
        if key not in daily or not daily[key]:
            raise ValueError(f"Saknar fältet {key} i prognosdata.")

    days = []
    for i in range(len(daily["time"])):
        days.append(
            {
                "date": daily["time"][i],
                "temp_max": daily["temperature_2m_max"][i],
                "temp_min": daily["temperature_2m_min"][i],
                "precipitation": daily["precipitation_sum"][i],
            }
        )
    return days


def calculate_average_max_temp(days):
    """Räknar ut medelvärdet av högsta temperatur med Pandas."""
    if not days:
        raise ValueError("Kan inte räkna ut medelvärde för en tom lista.")

    df = pd.DataFrame(days)
    mean_value = df["temp_max"].mean()
    return round(float(mean_value), 1)


def create_temperature_chart(days):
    """Skapar ett linjediagram över temperaturerna med Plotly."""
    if not days:
        return ""

    df = pd.DataFrame(days)
    fig = px.line(
        df,
        x="date",
        y=["temp_max", "temp_min"],
        labels={
            "date": "Datum",
            "value": "Temperatur (°C)",
            "variable": "Temperatur",
        },
        title="Temperaturprognos (3 dagar)",
        markers=True,
    )
    return fig.to_html(full_html=False, include_plotlyjs="cdn")
