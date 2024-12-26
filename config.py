import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

class AppConfig:
    WEATHER_API_TOKEN = os.getenv('WEATHER_API_KEY')
    DASH_DEBUG_MODE = os.getenv('DASH_DEBUG', 'True').lower() == 'true'
