import pytest

from app import app as flask_app


@pytest.fixture
def app():
    """Skapar och konfigurerar en instans av Flask-appen för testning."""
    flask_app.config.update(
        {
            "TESTING": True,
        }
    )
    return flask_app


@pytest.fixture
def client(app):
    """Skapar en testklient som vi använder för att göra HTTP-anrop i testerna."""
    return app.test_client()


@pytest.fixture
def fake_weather_data():
    """Skapar exempeldata som liknar ett riktigt svar från Open-Meteo API:et."""
    return {
        "current": {"temperature_2m": 12.5, "wind_speed_10m": 4.0},
        "daily": {
            "time": ["2026-05-01", "2026-05-02", "2026-05-03"],
            "temperature_2m_max": [15.0, 18.0, 12.0],
            "temperature_2m_min": [5.0, 7.0, 4.0],
            "precipitation_sum": [0.0, 1.5, 0.2],
        },
    }
