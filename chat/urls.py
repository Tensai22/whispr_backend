from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from chat.views import CommunityListView, CommunityCreateView, CommunityDetailView, \
    GroupListView, GroupCreateView, GroupDetailView, CommunityMembershipListView, GroupMembershipListView, MessageListView, \
    PrivateChatListCreateView, PrivateChatDetailView, PrivateChatMessagesView


from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import PrivateChatMessage, PrivateChat
from .serializers import PrivateChatMessageSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_messages(request, user_id):
    try:
        chat = PrivateChat.objects.filter(participants=request.user).filter(participants__id=user_id).first()
        if not chat:
            return Response({"detail": "Chat not found."}, status=404)

        messages = PrivateChatMessage.objects.filter(chat=chat).order_by('timestamp')
        serializer = PrivateChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"detail": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request, user_id):
    try:
        chat, created = PrivateChat.objects.get_or_create(
            participants=request.user,
            defaults={"participants": [request.user, user_id]}
        )
        message = PrivateChatMessage.objects.create(
            sender=request.user,
            chat=chat,
            text=request.data.get('text')
        )
        serializer = PrivateChatMessageSerializer(message)
        return Response(serializer.data)
    except Exception as e:
        return Response({"detail": str(e)}, status=500)



urlpatterns = [

    path('messages/<int:user_id>/', get_user_messages, name='get_user_messages'),
    path('messages/<int:user_id>/send/', send_message, name='send_message'),

    path('messages/', MessageListView.as_view(), name='message-list'),

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