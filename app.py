from flask import Flask, render_template, request

from weather_client import WeatherAPIError, fetch_weather
from weather_service import (
    CITIES,
    calculate_average_max_temp,
    create_temperature_chart,
    get_coordinates,
    is_valid_city,
    parse_current_weather,
    parse_daily_forecast,
)

app = Flask(__name__)


@app.template_filter("format_temp")
def format_temp(value):
    """Formaterar temperatur med en decimal och gradtecken (t.ex. 12,3 °C)."""
    if value is None:
        return "-"
    try:
        # Formaterar med 1 decimal och byter ut punkt mot kommatecken
        formatted = f"{float(value):.1f}".replace(".", ",")
        return f"{formatted} °C"
    except (ValueError, TypeError):
        return f"{value} °C"


@app.route("/")
def index():
    """Startsida där användaren väljer en stad."""
    return render_template("index.html", cities=list(CITIES.keys()))


@app.route("/forecast")
def forecast():
    """Visar väderprognos för den valda staden."""
    city = request.args.get("city")

    # Validera att staden finns i vår lista över tillåtna städer
    if not city or not is_valid_city(city):
        return (
            render_template(
                "forecast.html",
                error=f"'{city}' är inte en giltig stad. Välj en stad från listan.",
                city=city,
            ),
            400,
        )

    coords = get_coordinates(city)

    try:
        # Hämta rådata från Open-Meteo API:et
        raw_data = fetch_weather(coords["latitude"], coords["longitude"])

        # Tolka aktuell väderdata och 3-dagarsprognosen
        current = parse_current_weather(raw_data)
        days = parse_daily_forecast(raw_data)

        # Beräkna medeltemperatur med Pandas och skapa graf med Plotly
        avg_max_temp = calculate_average_max_temp(days)
        chart_html = create_temperature_chart(days)

        return render_template(
            "forecast.html",
            city=city,
            current=current,
            days=days,
            avg_max_temp=avg_max_temp,
            chart_html=chart_html,
        )
    except (WeatherAPIError, ValueError) as error:
        # Om API:et misslyckas eller datan är trasig visas felmeddelande med status 502
        return (
            render_template(
                "forecast.html",
                error=str(error),
                city=city,
            ),
            502,
        )


@app.errorhandler(404)
def page_not_found(error):
    """Visar 404-sida vid felaktig URL."""
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
