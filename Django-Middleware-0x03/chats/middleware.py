from django.http import HttpResponseForbidden
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        with open('requests.log', 'a') as f:
            f.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def get_current_time(self):
        return datetime.now().time()

    def __call__(self, request):
        now = self.get_current_time()
        start_time = datetime.strptime("18:00", "%H:%M").time()
        end_time = datetime.strptime("21:00", "%H:%M").time()

        if not (start_time <= now <= end_time):
            return HttpResponseForbidden("Access denied outside of 6 PM to 9 PM.")
        response = self.get_response(request)
        return response


# --- OffensiveLanguageMiddleware: Rate limit POSTs per IP ---
import time
from django.core.cache import cache

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit = 5  # messages
        self.time_window = 60  # seconds

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/api/messages'):
            ip = self.get_client_ip(request)
            now = int(time.time())
            window_key = f"msg_rate_{ip}_{now // self.time_window}"
            count = cache.get(window_key, 0)
            if count >= self.rate_limit:
                return HttpResponseForbidden("Rate limit exceeded: 5 messages per minute.")
            cache.set(window_key, count + 1, timeout=self.time_window)
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


# --- RolepermissionMiddleware: Only admin or moderator can access certain actions ---
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only allow admin or moderator to access /api/messages/ or /api/conversations/ endpoints
        if request.path.startswith('/api/messages') or request.path.startswith('/api/conversations'):
            user = getattr(request, 'user', None)
            if not (user and user.is_authenticated and getattr(user, 'role', None) in ['admin', 'moderator']):
                return HttpResponseForbidden("Only admin or moderator users can access this endpoint.")
        return self.get_response(request)
