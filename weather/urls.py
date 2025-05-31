from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'locations', views.LocationViewSet)
router.register(r'weather-records', views.WeatherRecordViewSet)
router.register(r'favorites', views.UserFavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', views.index, name='weather_index'),
    path('get-weather/', views.get_weather, name='get_weather'),
    path('api/', include(router.urls)),
] 