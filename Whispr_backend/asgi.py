"""
ASGI config for Whispr_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from chat import routing  # импорт ваших маршрутов websocket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = ProtocolTypeRouter(
   {
    "http": get_asgi_application(),
    "websocket": URLRouter(
         routing.websocket_urlpatterns
    ),
})
ASGI_APPLICATION = 'Whispr_backend.asgi.application'

