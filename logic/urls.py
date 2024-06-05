# urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view, register_view, logout_view, ProfileUpdateView, password_change_view, password_reset_view, password_reset_confirm_view, SendMessageView, ReceivedMessagesView, profile_view, search_users, send_message

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('id/<int:id>', profile_view, name='profile'),
    path('profile/', ProfileUpdateView.as_view(), name='user-profile'),
    #path('profile/password_change/', password_change_view, name='password_change'),
    path('password_reset/', password_reset_view, name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),
    path('send/', SendMessageView.as_view(), name='send_message'),
    path('received/', ReceivedMessagesView.as_view(), name='received_messages'),
    path('search_users/', search_users, name='search_users'),
    path('send_message/', send_message, name='send_message'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)