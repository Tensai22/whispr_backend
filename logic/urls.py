# urls.py
from django.urls import path
from .views import login_view, register_view, logout_view, password_reset_view

urlpatterns = [
    path('api/login/', login_view, name='login'),
    path('api/register/', register_view, name='register'),
    path('api/logout', logout_view, name='logout'),
    path('api/password_reset', password_reset_view, name='password_reset'),
]