from dash import Dash, dcc, html
import plotly.graph_objs as go
from weather.data_processing import transform_weather_data  # Обновлено имя функции

def initialize_dash_app(flask_app):
    """
    Инициализирует Dash-приложение с привязкой к Flask.

    :param flask_app: Экземпляр Flask-приложения.
    :return: Экземпляр Dash-приложения.
    """
    dash_app = Dash(__name__, server=flask_app, url_base_pathname='/dashboard/')
    dash_app.layout = html.Div(id="dashboard-container")
    return dash_app

def refresh_dash_content(dash_app, weather_data):
    """
    Обновляет содержимое Dash-приложения на основе погодных данных.

    :param dash_app: Экземпляр Dash-приложения.
    :param weather_data: Данные о погоде для построения графиков.
    """
    content = []

    for index, city_weather in enumerate(weather_data):
        city_name = city_weather.get('city', 'Неизвестный город')

        if 'hourly' in city_weather:
            df = transform_weather_data(city_weather)  # Используем новую функцию

            temp_graph = go.Figure(
                data=[go.Scatter(x=df['time'], y=df['temperature'], mode='lines', name='Температура')],
                layout=go.Layout(title=f'Температура в {city_name}', xaxis_title='Время', yaxis_title='°C')
            )

            wind_graph = go.Figure(
                data=[go.Scatter(x=df['time'], y=df['wind_speed'], mode='lines', name='Скорость ветра')],
                layout=go.Layout(title=f'Скорость ветра в {city_name}', xaxis_title='Время', yaxis_title='км/ч')
            )

            content.append(html.Div([
                html.H3(f'Прогноз для {city_name}'),
                dcc.Graph(figure=temp_graph, style={'height': '400px'}),
                dcc.Graph(figure=wind_graph, style={'height': '400px'})
            ]))

    dash_app.layout = html.Div(content)
