from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

#from .views import *
from .views import login_view, register_view, logout_view, profile_update_view, password_change_view, \
    password_reset_view, password_reset_confirm_view, SendMessageView, ReceivedMessagesView, profile_view, UserViewSet, \
    ChatViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('id/<int:id>', profile_view, name='profile'),
    path('profile/update/', profile_update_view.as_view(), name='profile_update'),
    #path('profile/password_change/', password_change_view, name='password_change'),
    path('password_reset/', password_reset_view, name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),
    path('send/', SendMessageView.as_view(), name='send_message'),
    path('received/', ReceivedMessagesView.as_view(), name='received_messages'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)