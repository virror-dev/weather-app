from unittest.mock import patch

from weather_client import WeatherAPIError


def test_index_route(client):
    """Testar att startsidan svarar med statuskod 200 och visar stadsväljaren."""
    response = client.get("/")

    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "Väderappen" in html
    assert "Välj en stad" in html
    assert "Stockholm" in html
    assert "Göteborg" in html


def test_forecast_valid_city(client, fake_weather_data):
    """Testar väderprognosen för en giltig stad med ett mockat API-svar."""
    with patch("app.fetch_weather", return_value=fake_weather_data):
        response = client.get("/forecast?city=Stockholm")

        assert response.status_code == 200
        html = response.data.decode("utf-8")
        assert "Väder i Stockholm" in html
        assert "12,5 °C" in html
        assert "4.0 m/s" in html
        assert "Prognos för 3 dagar" in html
        assert "Temperaturprognos" in html


def test_forecast_invalid_city(client):
    """Testar att statuskod 400 och felmeddelande visas vid ogiltig stad."""
    response = client.get("/forecast?city=Uppsala")

    assert response.status_code == 400
    html = response.data.decode("utf-8")
    assert "Ett fel uppstod" in html
    assert "Uppsala" in html
    assert "inte en giltig stad" in html


def test_forecast_missing_city(client):
    """Testar att felmeddelande och kod 400 visas om stadsparametern saknas."""
    response = client.get("/forecast")

    assert response.status_code == 400
    html = response.data.decode("utf-8")
    assert "Ett fel uppstod" in html


def test_forecast_api_error(client):
    """Testar att statuskod 502 visas om väder-API:et kastar ett fel."""
    with patch(
        "app.fetch_weather",
        side_effect=WeatherAPIError("Kunde inte hämta väderdata från API:et just nu."),
    ):
        response = client.get("/forecast?city=Stockholm")

        assert response.status_code == 502
        html = response.data.decode("utf-8")
        assert "Ett fel uppstod" in html
        assert "Kunde inte hämta väderdata från API:et just nu." in html


def test_404_page(client):
    """Testar att vår 404-sida visas med statuskod 404 vid ogiltig URL."""
    response = client.get("/ogiltig-url-som-saknas")

    assert response.status_code == 404
    html = response.data.decode("utf-8")
    assert "404" in html
    assert "Sidan du letar efter kunde inte hittas" in html


def test_format_temp_filter(app):
    """Testar att vårt anpassade Jinja-filter formaterar temperatur med komma och °C."""
    filter_func = app.jinja_env.filters["format_temp"]
    assert filter_func(12.3) == "12,3 °C"
    assert filter_func(0.0) == "0,0 °C"
    assert filter_func(-4.5) == "-4,5 °C"
    assert filter_func(None) == "-"
