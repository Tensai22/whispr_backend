"""
ASGI config for Whispr_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Whispr_backend.settings')
django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter(
    {
        'http' : get_asgi_application(),
        'websocket' : AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        )

    }
)

ASGI_APPLICATION = 'Whispr_backend.asgi.application'

