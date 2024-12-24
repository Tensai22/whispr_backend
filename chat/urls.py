from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from chat import views
from chat.views import CommunityListView, CommunityCreateView, CommunityDetailView, \
    GroupListView, GroupCreateView, GroupDetailView, CommunityMembershipListView, GroupMembershipListView, MessageListView, \
    PrivateChatListCreateView, PrivateChatDetailView, PrivateChatMessagesView

urlpatterns = [
    path('messages/', views.MessageListView.as_view(), name='message-list'),

    path('communities/', CommunityListView.as_view(), name='community-list'),
    path('communities/create/', CommunityCreateView.as_view(), name='community-create'),
    path('communities/<int:pk>/', CommunityDetailView.as_view(), name='community-detail'),
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('groups/create/', GroupCreateView.as_view(), name='group-create'),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    path('community-memberships/', CommunityMembershipListView.as_view(), name='community-memberships-list'),
    path('group-memberships/', GroupMembershipListView.as_view(), name='group-memberships-list'),

    path('private-chats/', PrivateChatListCreateView.as_view(), name='private-chat-list-create'),
    path('private-chats/<int:pk>/', PrivateChatDetailView.as_view(), name='private-chat-detail'),
    path('private-chats/<int:pk>/messages/', PrivateChatMessagesView.as_view(), name='private-chat-messages'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)