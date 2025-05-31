from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}, {self.country}"

    class Meta:
        ordering = ['-created_at']

class WeatherRecord(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='weather_records')
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.IntegerField()
    pressure = models.IntegerField()
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=200)
    recorded_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Weather for {self.location.name} at {self.recorded_at}"

    class Meta:
        ordering = ['-recorded_at']

class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.location.name}"

    class Meta:
        unique_together = ['user', 'location']
        ordering = ['-created_at']
