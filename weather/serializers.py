from rest_framework import serializers
from .models import Location, WeatherRecord, UserFavorite

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'latitude', 'longitude', 'country', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class WeatherRecordSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)

    class Meta:
        model = WeatherRecord
        fields = ['id', 'location', 'location_name', 'temperature', 'humidity', 'pressure', 
                 'wind_speed', 'description', 'recorded_at', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class UserFavoriteSerializer(serializers.ModelSerializer):
    location_details = LocationSerializer(source='location', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserFavorite
        fields = ['id', 'user', 'user_username', 'location', 'location_details', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at'] 