from django.contrib import admin
from .models import Weather, Temperature, Precipitation, WeatherStation, Datetime

admin.site.register(Weather)
admin.site.register(Temperature)
admin.site.register(Precipitation)
admin.site.register(WeatherStation)
admin.site.register(Datetime)
