# urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view, register_view, logout_view, password_change_view, password_reset_view, password_reset_confirm_view, SendMessageView, ReceivedMessagesView

urlpatterns = [
    path('api/login/', login_view, name='login'),
    path('api/register/', register_view, name='register'),
    path('api/logout', logout_view, name='logout'),
    path('api/passord_change', password_change_view, name='password_change'),
    path('api/password_reset', password_reset_view, name='password_reset'),
    path('api/password_reset_confirm/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),
    path('send/', SendMessageView.as_view(), name='send_message'),
    path('received/', ReceivedMessagesView.as_view(), name='received_messages'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)