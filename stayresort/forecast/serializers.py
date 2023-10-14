from rest_framework import serializers

class ForecastSerializer(serializers.Serializer):
    forecast = serializers.ListField(child=serializers.FloatField())
