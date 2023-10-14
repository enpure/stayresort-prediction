from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from .serializers import ForecastSerializer
from .predictor import get_forecast
import os
from django.conf import settings
import pandas as pd

def index(request):
    return render(request, 'index.html')

data_path = os.path.join(settings.BASE_DIR, 'media', 'Cleaned_Balance_Stay.xlsx')
data = pd.read_excel(data_path)



@api_view(['GET'])
@renderer_classes([JSONRenderer])
def balance_forecast_view(request):
    profits_image, _, _ = get_forecast(plot_graphs=True)  # Получаем изображение для прибыли

    if profits_image:
        response = HttpResponse(content_type="image/png")
        response.write(profits_image.getvalue())  # Get the Profits forecast image
        return response

    return JsonResponse({"message": "No graph generated."})

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def profits_forecast_view(request):
    _, _, income_spends_image = get_forecast(plot_graphs=True)  # Получаем изображение для доходов и расходов

    if income_spends_image:
        response = HttpResponse(content_type="image/png")
        response.write(income_spends_image.getvalue())  # Get the Income & Spends forecast image
        return response

    return JsonResponse({"message": "No graph generated."})

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def income_spends_forecast_view(request):
    _, balance_image, _ = get_forecast(plot_graphs=True)  # Получаем изображение для баланса

    if balance_image:
        response = HttpResponse(content_type="image/png")
        response.write(balance_image.getvalue())  # Get the Balance forecast image
        return response

    return JsonResponse({"message": "No graph generated."})
