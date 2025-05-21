from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('process-file/', views.process_file, name='process-file')
]