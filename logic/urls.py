# urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import logout_view, password_change_view, \
    password_reset_view, password_reset_confirm_view, profile_view, search_users, UserProfileView, LoginView, \
    RegistrationView, ProfileUpdateView, update_avatar
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('id/<int:id>', profile_view, name='profile'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('change_password/', password_change_view, name='password_change'),
    path('password_reset/', password_reset_view, name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),
    path('update-avatar/', update_avatar, name='update-avatar'),
    path('search_users/', search_users, name='search_users'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)