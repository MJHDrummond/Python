from django.http import HttpResponse
from django.template import loader
from .models import Weather, Datetime
from datetime import datetime

def index(request):
    try:
        latest_weather_list = Weather.objects.order_by('-id')[:5]
        template = loader.get_template('weather/index.html')
        context = {'latest_weather_list': latest_weather_list}
        return HttpResponse(template.render(context, request))
    except Weather.DoesNotExist:
        return generate_error(request, "No saved Weather found.")


def detail(request, weather_id):
    try:
        weather = Weather.objects.get(id=weather_id)
        template = loader.get_template('weather/detail.html')
        context = {'weather': weather}
        return HttpResponse(template.render(context, request))
    except Weather.DoesNotExist:
        return generate_error(request, f"No Weather Details found for id: {weather_id}")

def get_latest_weather(request):
    try:
        current_datetime = datetime.now()
        weather = Datetime.objects.get(
            measurement_date=current_datetime.strftime("%Y-%m-%d"),
            measurement_hour=current_datetime.hour)
        return HttpResponse("Weather is already up-to-date")
    except Datetime.DoesNotExist:
        return HttpResponse("Updating weather")

def generate_error(request, error_message):
        template = loader.get_template('weather/error.html')
        context = {'error_message': error_message}
        return HttpResponse(template.render(context, request))
