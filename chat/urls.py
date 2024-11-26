from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from chat import views
from chat.views import send_message, get_messages, CommunityListView, CommunityCreateView, CommunityDetailView, \
    GroupListView, GroupCreateView, GroupDetailView, CommunityMembershipListView, GroupMembershipListView

urlpatterns = [
    path('', views.index, name='index'),  # Страница списка комнат или чата
    path('get_messages/', views.GetMessagesView.as_view(), name='get_messages'),
    path('send_message/', send_message, name='send_message'),

    path('communities/', CommunityListView.as_view(), name='community-list'),
    path('communities/create/', CommunityCreateView.as_view(), name='community-create'),
    path('communities/<int:pk>/', CommunityDetailView.as_view(), name='community-detail'),
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('groups/create/', GroupCreateView.as_view(), name='group-create'),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    path('community-memberships/', CommunityMembershipListView.as_view(), name='community-memberships-list'),
    path('group-memberships/', GroupMembershipListView.as_view(), name='group-memberships-list'),
]
