from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:weather_id>/', views.detail, name='detail'),
    path('get-latest-weather/', views.get_latest_weather, name='get-latest-weather')
]