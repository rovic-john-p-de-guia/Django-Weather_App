import time
from functools import wraps
from django.core.cache import cache
from django.http import JsonResponse

# Settings
RATE_LIMIT = 10  # max requests
TIME_WINDOW = 60  # seconds

def rate_limit(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Use user id if authenticated, else use IP
        if request.user.is_authenticated:
            ident = f"rl:{request.user.pk}"
        else:
            ident = f"rl:{request.META.get('REMOTE_ADDR')}"
        
        now = int(time.time())
        window_key = f"{ident}:{now // TIME_WINDOW}"
        count = cache.get(window_key)
        if count is None:
            cache.set(window_key, 1, TIME_WINDOW)
        else:
            if count >= RATE_LIMIT:
                return JsonResponse({
                    "error": "Rate limit exceeded. Try again later."
                }, status=429)
            cache.incr(window_key)
        return view_func(request, *args, **kwargs)
    return _wrapped_view