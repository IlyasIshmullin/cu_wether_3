import pandas as pd

def transform_weather_data(weather_json):
    """
    Преобразует JSON с погодными данными в DataFrame для визуализации.

    :param weather_json: JSON с данными о погоде.
    :return: DataFrame с временными рядами температур, осадков и ветра.
    """
    hourly_data = weather_json.get('hourly', {})

    data_frame = pd.DataFrame({
        'time': hourly_data.get('time', []),
        'temperature': hourly_data.get('temperature_2m', []),
        'humidity': hourly_data.get('relative_humidity_2m', []),
        'precipitation': hourly_data.get('rain', []),
        'wind_speed': hourly_data.get('wind_speed_10m', [])
    })

    # Преобразуем строковые даты в datetime
    data_frame['time'] = pd.to_datetime(data_frame['time'])
    return data_frame
