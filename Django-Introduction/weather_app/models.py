from django.db import models

class WeatherStation(models.Model):
    station_number = models.IntegerField()
    def __str__(self):
        return str(self.station_number)

class Temperature(models.Model):
    minimum_hourly_temperature_celsius = models.DecimalField(decimal_places=2, max_digits=4)
    def __str__(self):
        return str(self.minimum_hourly_temperature_celsius)

class Precipitation(models.Model):
    maximum_hourly_precipitation_millimeters = models.DecimalField(decimal_places=2, max_digits=5)
    def __str__(self):
        return str(self.maximum_hourly_precipitation_millimeters)

class Datetime(models.Model):
    measurement_hour = models.IntegerField()
    measurement_date = models.DateField()
    def __str__(self):
        return str(self.measurement_date) + ' ' + str(self.measurement_hour) + ':00:00'

class Weather(models.Model):
    weather_station = models.ForeignKey(WeatherStation, on_delete=models.DO_NOTHING)
    temperature = models.ForeignKey(Temperature, on_delete=models.DO_NOTHING)
    precipitation = models.ForeignKey(Precipitation, on_delete=models.DO_NOTHING)
    datetime = models.ForeignKey(Datetime, on_delete=models.DO_NOTHING)
