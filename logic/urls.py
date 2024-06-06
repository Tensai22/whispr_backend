# urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view, register_view, logout_view, profile_update_view, password_change_view, \
    password_reset_view, password_reset_confirm_view, profile_view, search_users, \
    send_message, get_messages

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('id/<int:id>', profile_view, name='profile'),
    path('profile/update/', profile_update_view.as_view(), name='profile_update'),
    #path('profile/password_change/', password_change_view, name='password_change'),
    path('password_reset/', password_reset_view, name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),


    path('search_users/', search_users, name='search_users'),

    path('send_message/', send_message, name='send_message'),
    path('get_messages/', get_messages, name='get_messages'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)