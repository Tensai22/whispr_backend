from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Страница списка комнат или чата
    path('api/get_messages/', views.GetMessagesView.as_view(), name='get_messages'),  # API для получения сообщений
]
