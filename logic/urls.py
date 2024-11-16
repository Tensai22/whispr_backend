# urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view, register_view, logout_view, profile_update_view, password_change_view, \
    password_reset_view, password_reset_confirm_view, profile_view, search_users, \
    send_message, get_messages, MyTokenObtainPairView, MyTokenRefreshView, \
    GroupListView, GroupCreateView, GroupDetailView, GroupMembershipListView, \
    CommunityListView, CommunityDetailView, CommunityCreateView, CommunityMembershipListView

urlpatterns = [
    # path('login/', login_view, name='login'),
    # path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('id/<int:id>', profile_view, name='profile'),
    path('update/', profile_update_view.as_view(), name='profile_update'),
    path('change_password/', password_change_view, name='password_change'),
    path('password_reset/', password_reset_view, name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),

    path('search_users/', search_users, name='search_users'),

    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register_view, name='register'),
    path('send_message/', send_message, name='send_message'),
    path('get_messages/', get_messages, name='get_messages'),

    path('communities/', CommunityListView.as_view(), name='community-list'),
    path('communities/create/', CommunityCreateView.as_view(), name='community-create'),
    path('communities/<int:pk>/', CommunityDetailView.as_view(), name='community-detail'),
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('groups/create/', GroupCreateView.as_view(), name='group-create'),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    path('community-memberships/', CommunityMembershipListView.as_view(), name='community-memberships-list'),
    path('group-memberships/', GroupMembershipListView.as_view(), name='group-memberships-list'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)