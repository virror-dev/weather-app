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
    """Formaterar temperatur med gradtecken (°C)."""
    if value is None:
        return "-"
    return f"{value} °C"


@app.route("/")
def index():
    """Startsida där användaren väljer en stad."""
    return render_template("index.html", cities=list(CITIES.keys()))


@app.route("/forecast")
def forecast():
    """Visar väderprognos för den valda staden."""
    city = request.args.get("city")

    if not city or not is_valid_city(city):
        return render_template(
            "forecast.html",
            error=f"'{city}' är inte en giltig stad. Välj en stad från listan.",
            city=city,
        )

    coords = get_coordinates(city)

    try:
        raw_data = fetch_weather(coords["latitude"], coords["longitude"])
        current = parse_current_weather(raw_data)
        days = parse_daily_forecast(raw_data)
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
        return render_template(
            "forecast.html",
            error=str(error),
            city=city,
        )


@app.errorhandler(404)
def page_not_found(error):
    """Visar 404-sida vid felaktig URL."""
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
