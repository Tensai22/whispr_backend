from django.utils import timezone
from datetime import timedelta
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest
class LastActiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        user = request.user
        if request.user.is_authenticated:
            profile = getattr(request.user, 'profile', None)
            if profile:
                now = timezone.now()
                if profile.last_activity < now - timedelta(minutes=2):
                    profile.last_activity = now
                    profile.save()

        response = self.get_response(request)

        return response