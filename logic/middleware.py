# logic/middleware.py

from django.utils import timezone
from datetime import timedelta
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest
import logging

logger = logging.getLogger(__name__)

class LastActiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        logger.debug('LastActiveMiddleware called')
        user = request.user
        if user.is_authenticated:
            profile = getattr(user, 'profile', None)
            if profile:
                now = timezone.now()
                if profile.last_activity < now - timedelta(minutes=2):
                    profile.last_activity = now
                    profile.save()
                    logger.debug(f'Updated last_activity for user {user.id}')
                else:
                    logger.debug(f'Profile last activity for user {user.id} is recent enough.')

        response = self.get_response(request)
        logger.debug('LastActiveMiddleware finished processing')

        return response

class SetUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.debug('SetUserMiddleware called')
        if request.user.is_authenticated:
            request.user = request.user
        else:
            request.user = None
        logger.debug('SetUserMiddleware finished processing')
