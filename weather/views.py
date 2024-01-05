from datetime import datetime

import requests
from django.shortcuts import render

from .forms import CityForm


def index(request):
    url_forecast = 'https://api.openweathermap.org/data/2.5/forecast/daily?q={}&cnt=7&appid=271d1234d3f497eed5b1d80a07b3fcd1'

    if request.method == 'GET' and 'city' in request.GET:
        selected_city = request.GET['city']
        city_weather = requests.get(url_forecast.format(selected_city)).json()

        weather_forecast_data = {}

        for forecast in city_weather['list']:
            timestamp = forecast['dt']
            date_time = datetime.utcfromtimestamp(timestamp)
            date = date_time.date()
            formatted_date = date.strftime("%A, %d %B %Y")

            weather = {
                'date': formatted_date,
                'temperature': forecast['temp']['day'] - 273.15,
                'temperature_min': forecast['temp']['min'] - 273.15,
                'temperature_max': forecast['temp']['max'] - 273.15,
                'description': forecast['weather'][0]['description'],
                'humidity': forecast['humidity'],
            }

            if formatted_date not in weather_forecast_data:
                weather_forecast_data[formatted_date] = []

            weather_forecast_data[formatted_date].append(weather)

        context = {'selected_city': selected_city, 'weather_forecast_data': weather_forecast_data}
        return render(request, 'weather/index.html', context)

    form = CityForm()
    context = {'form': form}
    return render(request, 'weather/index.html', context)
