from django.urls import path
from .views import generate_forecast, show_forecast_form, home, dashboard

app_name = 'predictions'


urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('generate-forecast/', generate_forecast, name='generate_forecast'),
    path('forecast-form/', show_forecast_form, name='show_forecast_form'),
]
