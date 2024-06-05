from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from chat import views as chat_views
urlpatterns = [

    path('', chat_views.chat_view, name='chat-page'),

    #сессия логина
    path('auth/login/', LoginView.as_view
        (template_name='chat/LoginPage.html'), name='login-user'),
    path('auth/logout/', LogoutView.as_view(), name='logout-user'),
]