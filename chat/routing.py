from django.urls import path, include
from chat.consumers import ChatConsumer

#Роутер чата который реализует функцию
websocket_urlpatterns = [
    path('', ChatConsumer.as_asgi()),
]
