import pytest

from weather_service import (
    calculate_average_max_temp,
    create_temperature_chart,
    get_coordinates,
    is_valid_city,
    parse_current_weather,
    parse_daily_forecast,
)


# Testar giltiga städer, ogiltig stad, tom sträng och små bokstäver
@pytest.mark.parametrize(
    "city, expected",
    [
        ("Stockholm", True),
        ("Göteborg", True),
        ("Malmö", True),
        ("Umeå", True),
        ("Kiruna", True),
        ("Uppsala", False),
        ("stockholm", False),
        ("", False),
    ],
)
def test_is_valid_city(city, expected):
    assert is_valid_city(city) == expected


def test_get_coordinates():
    # Kollar att rätt koordinater returneras för en giltig stad
    coords = get_coordinates("Stockholm")
    assert coords == {"latitude": 59.33, "longitude": 18.07}

    # Kollar att en ogiltig stad returnerar None
    assert get_coordinates("Uppsala") is None


def test_parse_current_weather_valid():
    """Testar att nuvarande väder tolkas rätt."""
    api_data = {"current": {"temperature_2m": 14.2, "wind_speed_10m": 5.1}}
    result = parse_current_weather(api_data)
    assert result == {"temperature": 14.2, "wind_speed": 5.1}


def test_parse_daily_forecast_valid():
    """Testar att API-svaret görs om till en lista med tre dagar."""
    api_data = {
        "daily": {
            "time": ["2026-05-01", "2026-05-02", "2026-05-03"],
            "temperature_2m_max": [15.0, 18.0, 12.0],
            "temperature_2m_min": [5.0, 7.0, 4.0],
            "precipitation_sum": [0.0, 1.5, 0.2],
        }
    }

    days = parse_daily_forecast(api_data)

    assert len(days) == 3
    assert days[0] == {
        "date": "2026-05-01",
        "temp_max": 15.0,
        "temp_min": 5.0,
        "precipitation": 0.0,
    }


# Testar att funktionen hanterar tomma eller ofullständiga svar från API:et
@pytest.mark.parametrize(
    "bad_data",
    [
        {},
        {"daily": {}},
        {"daily": {"time": []}},
        {"daily": {"time": ["2026-05-01"]}},
    ],
)
def test_parse_daily_forecast_invalid_data(bad_data):
    with pytest.raises(ValueError):
        parse_daily_forecast(bad_data)


# Testar uträkning av medelvärde med Pandas för olika temperaturlistor
@pytest.mark.parametrize(
    "days, expected_avg",
    [
        (
            [
                {"temp_max": 10.0},
                {"temp_max": 20.0},
                {"temp_max": 15.0},
            ],
            15.0,
        ),
        (
            [
                {"temp_max": -5.0},
                {"temp_max": 0.0},
                {"temp_max": 2.0},
            ],
            -1.0,
        ),
    ],
)
def test_calculate_average_max_temp(days, expected_avg):
    assert calculate_average_max_temp(days) == expected_avg


def test_create_temperature_chart():
    """Testar att Plotly skapar HTML-kod för diagrammet."""
    days = [
        {"date": "2026-05-01", "temp_max": 15.0, "temp_min": 5.0},
        {"date": "2026-05-02", "temp_max": 18.0, "temp_min": 7.0},
    ]
    chart_html = create_temperature_chart(days)

    assert "<div" in chart_html
    assert "Temperaturprognos" in chart_html
