from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('temperature/', views.temperature, name='temperature'),
    path('humidity/', views.humidity, name='humidity'),
    path('luminosity/', views.luminosity, name='luminosity'),
    path('history/', views.history, name='history'),
    path('reports/', views.reports, name='reports'),
    path('dashboard/', views.sensors_dashboard, name='sensors_dashboard'),
    path('api/sensor-data/', api.sensor_data, name='sensor_data'),
]
