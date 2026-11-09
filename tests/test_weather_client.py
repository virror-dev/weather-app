from unittest.mock import MagicMock, patch

import pytest
import requests

from weather_client import WeatherAPIError, fetch_weather


def test_fetch_weather_success():
    """Testar att fetch_weather returnerar JSON-data när API:et svarar OK."""
    fake_data = {
        "current": {"temperature_2m": 10.5, "wind_speed_10m": 3.2},
        "daily": {
            "time": ["2026-05-01", "2026-05-02", "2026-05-03"],
            "temperature_2m_max": [12.0, 14.0, 11.0],
            "temperature_2m_min": [4.0, 5.0, 3.0],
            "precipitation_sum": [0.0, 2.1, 0.0],
        },
    }

    # Skapar låtsassvar som ett riktigt svar från requests
    mock_response = MagicMock()
    mock_response.json.return_value = fake_data

    # Ersätter requests.get med vår mock under testet
    with patch("weather_client.requests.get", return_value=mock_response) as mock_get:
        result = fetch_weather(59.33, 18.07)

        assert result == fake_data
        # Kontrollerar att anropet gjordes och att raise_for_status anropades
        mock_get.assert_called_once()
        mock_response.raise_for_status.assert_called_once()


def test_fetch_weather_timeout():
    """Testar att en Timeout från requests görs om till vårt eget WeatherAPIError."""
    with patch("weather_client.requests.get", side_effect=requests.Timeout):
        with pytest.raises(WeatherAPIError, match="Kunde inte hämta väderdata"):
            fetch_weather(59.33, 18.07)


def test_fetch_weather_http_error():
    """Testar att ett HTTP-fel (t.ex. 500) görs om till WeatherAPIError."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")

    with patch("weather_client.requests.get", return_value=mock_response):
        with pytest.raises(WeatherAPIError, match="Kunde inte hämta väderdata"):
            fetch_weather(59.33, 18.07)
