from flask import Flask, render_template, request, jsonify
import json

from weather.dash_app import initialize_dash_app, refresh_dash_content
from weather.api import fetch_weather_by_city, fetch_weather_by_coords, fetch_city_coordinates

# Создание экземпляра Flask-приложения
app = Flask(__name__)

# Инициализация Dash-приложения
app_dash = initialize_dash_app(app)

@app.route("/", methods=["GET", "POST"])
def homepage():
    """
    Главная страница с формой для ввода маршрута.
    """
    if request.method == "POST":
        # Извлечение данных из формы
        start_location = request.form.get("start_city") or (
            request.form.get("latitude"), request.form.get("longitude")
        )
        end_city = request.form.get("end_city")
        forecast_days = int(request.form.get("forecast_days", 1))
        intermediate_count = int(request.form.get("num_intermediate_points", 0))

        # Список промежуточных городов
        intermediate_cities = [
            request.form.get(f"intermediate_city_{i}") for i in range(intermediate_count)
        ]

        # Подготовка списка точек маршрута
        route_points = [start_location] + intermediate_cities + [end_city]
        weather_data = []

        # Запрос данных погоды для каждой точки маршрута
        for point in route_points:
            if isinstance(point, tuple):  # Если это координаты
                weather_info = fetch_weather_by_coords(*point, days=forecast_days)
                if "city" not in weather_info or not weather_info["city"]:
                    city_name = fetch_city_coordinates(point).get("city", "Неизвестный город")
                    weather_info["city"] = city_name
            else:  # Если это название города
                weather_info = fetch_weather_by_city(point, days=forecast_days)
                if not weather_info.get("city"):
                    weather_info["city"] = point
            weather_data.append(weather_info)

        # Обновление контента Dash-приложения
        refresh_dash_content(app_dash, weather_data)

        # Рендеринг страницы с графиками
        return render_template("graphs.html", weather_data=weather_data)

    return render_template("form.html")

@app.route("/graphs")
def display_graphs():
    """
    Страница с графиками прогноза погоды.
    """
    return render_template("graphs.html")

@app.route("/map")
def display_map():
    """
    Страница с отображением карты городов.
    """
    raw_cities = request.args.get("cities")
    cities_data = json.loads(raw_cities) if raw_cities else []
    return render_template("map.html", cities=cities_data)

if __name__ == "__main__":
    app.run(debug=True)
