from django.urls import path
from . import views
from .views import GetMessagesView

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('api/get_messages/<str:room_name>/', GetMessagesView.as_view(), name='get_messages'),
]