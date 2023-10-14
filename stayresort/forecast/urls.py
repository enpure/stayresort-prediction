from django.urls import path
from .views import balance_forecast_view, income_spends_forecast_view, profits_forecast_view
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('balance_forecast/', balance_forecast_view, name="balance_forecast"),
    path('income_spends_forecast/', income_spends_forecast_view, name="income_spends_forecast"),
    path('profits_forecast/', profits_forecast_view, name="profits_forecast"),
]
