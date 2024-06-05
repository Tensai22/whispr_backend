from django.urls import path
from .views import MessageListCreateView

urlpatterns = [
    path('', MessageListCreateView.as_view(), name='chat'),
]
