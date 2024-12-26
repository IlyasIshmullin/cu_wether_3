import requests
from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()
API_KEY = os.getenv('WEATHER_API_KEY')


def fetch_city_coordinates(city_name):
    """
    Получает координаты по названию города.

    :param city_name: Название города для поиска.
    :return: Словарь с широтой и долготой или None в случае ошибки.
    """
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ru&format=json"
        response = requests.get(url)
        response.raise_for_status()
        result = response.json().get('results', [{}])[0]
        return {
            'latitude': result.get('latitude'),
            'longitude': result.get('longitude')
        }
    except Exception as error:
        print(f"Ошибка получения координат для города {city_name}: {error}")
        return None


def fetch_weather_by_coords(latitude, longitude, days=1):
    """
    Получает погодные данные по координатам.

    :param latitude: Широта местоположения.
    :param longitude: Долгота местоположения.
    :param days: Количество дней для прогноза.
    :return: JSON-данные с прогнозом погоды.
    """
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}&hourly=temperature_2m," 
            f"relative_humidity_2m,rain,wind_speed_10m&forecast_days={days}"
        )
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as network_error:
        print(f"Ошибка сети: {network_error}")
        return None
    except Exception as generic_error:
        print(f"Произошла ошибка: {generic_error}")
        return None


def fetch_weather_by_city(city_name, days=1):
    """
    Получает погодные данные по названию города.

    :param city_name: Название города.
    :param days: Количество дней для прогноза.
    :return: JSON-данные с прогнозом погоды.
    """
    try:
        coordinates = fetch_city_coordinates(city_name)
        if not coordinates:
            raise ValueError("Не удалось получить координаты города.")

        return fetch_weather_by_coords(
            latitude=coordinates['latitude'],
            longitude=coordinates['longitude'],
            days=days
        )
    except Exception as error:
        print(f"Ошибка получения данных погоды для города {city_name}: {error}")
        return None
