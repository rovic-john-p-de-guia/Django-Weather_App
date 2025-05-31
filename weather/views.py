from django.shortcuts import render
from django.conf import settings
import requests
from django.http import JsonResponse, HttpResponseForbidden
from django.core.cache import cache
import time
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'weather/index.html')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required
def get_weather(request):
    if request.method == 'POST':
        # --- Rate limiting ---
        ip = get_client_ip(request)
        key = f"weather_rate_{ip}"
        rate = cache.get(key, {'count': 0, 'start': time.time()})
        window = 600  # 10 minutes
        limit = 10    # 10 requests per window
        now = time.time()
        if now - rate['start'] > window:
            rate = {'count': 1, 'start': now}
        else:
            rate['count'] += 1
        cache.set(key, rate, timeout=window)
        if rate['count'] > limit:
            return HttpResponseForbidden('Rate limit exceeded. Please try again later.')
        # --- End rate limiting ---

        location = request.POST.get('location')
        if not location:
            return JsonResponse({'error': 'Location is required'}, status=400)

        url = (
            f"https://weather-api167.p.rapidapi.com/api/weather/forecast"
            f"?place={location}&cnt=1&units=metric&type=three_hour&mode=json&lang=en"
        )
        headers = {
            "x-rapidapi-key": settings.RAPIDAPI_KEY,
            "x-rapidapi-host": settings.RAPIDAPI_HOST,
            "Accept": "application/json"
        }
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            print("API response:", data)
            if response.status_code != 200 or "list" not in data or not data["list"]:
                return JsonResponse({'error': 'Weather data not available'}, status=404)

            forecast = data["list"][0]
            main = forecast["main"]
            weather = forecast["weather"][0]
            wind = forecast.get("wind", {})
            clouds = forecast.get("clouds", {})
            rain = forecast.get("rain", {})
            snow = forecast.get("snow", {})
            sys = forecast.get("sys", {})

            weather_info = {
                "location": location,
                "summary": weather.get("main"),
                "temperature": round(main.get("temp", 0)),
                "feels_like": main.get("feels_like"),
                "temp_min": main.get("temp_min"),
                "temp_max": main.get("temp_max"),
                "temperature_unit": "°C",
                "humidity": main.get("humidity"),
                "humidity_unit": "%",
                "pressure": main.get("pressure"),
                "pressure_unit": "hPa",
                "sea_level_pressure": main.get("sea_level"),
                "ground_level_pressure": main.get("grnd_level"),
                "description": weather.get("description"),
                "main_weather": weather.get("main"),
                "icon": weather.get("icon"),
                "wind_speed": wind.get("speed"),
                "wind_degrees": wind.get("deg"),
                "wind_direction": None,  # You can add logic to convert degrees to direction
                "wind_gust_speed": wind.get("gust"),
                "wind_speed_unit": "m/s",
                "cloudiness": clouds.get("all"),
                "cloudiness_unit": "%",
                "rain_amount": rain.get("3h"),
                "rain_unit": "mm",
                "snow_amount": snow.get("3h"),
                "snow_unit": "mm",
                "visibility_distance": forecast.get("visibility"),
                "visibility_unit": "m",
                "probability_of_precipitation": forecast.get("pop"),
                "probability_of_precipitation_unit": "%",
                "part_of_day": sys.get("pod") if sys else None,
                "datetime": forecast.get("dt_txt"),
            }
            return JsonResponse(weather_info)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
