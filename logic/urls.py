# urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view, register_view, logout_view, password_change_view, password_reset_view, \
    password_reset_confirm_view, SendMessageView, ReceivedMessagesView, search_users

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('password_change/', password_change_view, name='password_change'),
    path('password_reset/', password_reset_view, name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),
    path('send/', SendMessageView.as_view(), name='send_message'),
    path('received/', ReceivedMessagesView.as_view(), name='received_messages'),
    path('search_users/', search_users, name='search_users'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)