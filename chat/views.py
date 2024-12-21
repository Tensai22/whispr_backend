import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Message, Group, GroupMembership, Chat, CommunityMembership, Community, PrivateChat, \
    PrivateChatMessage
from .serializers import CommunitySerializer, CommunityMembershipSerializer, GroupSerializer, \
    GroupMembershipSerializer, MessageSerializer, PrivateChatSerializer, PrivateChatMessageSerializer


def index(request):
    return render(request, 'chat/index.html')

#Резерв
'''
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
'''
# Create your views here.
def room(request, room_name):

    messages = Message.objects.filter(room_name=room_name).order_by('timestamp')
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': messages
    })

class MessageListView(ListAPIView):
    queryset = Message.objects.all().order_by('timestamp')
    serializer_class = MessageSerializer

class GroupListView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class GroupCreateView(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class GroupDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

class GroupMembershipListView(ListAPIView):
    queryset = GroupMembership.objects.all()
    serializer_class = GroupMembershipSerializer
    permission_classes = [IsAuthenticated]


class CommunityListView(ListAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]


class CommunityCreateView(ListCreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]


class CommunityDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]


class CommunityMembershipListView(ListAPIView):
    queryset = CommunityMembership.objects.all()
    serializer_class = CommunityMembershipSerializer
    permission_classes = [IsAuthenticated]


class PrivateChatListCreateView(ListCreateAPIView):
    serializer_class = PrivateChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.private_chats.all()

    def perform_create(self, serializer):
        serializer.save(participants=[self.request.user] + list(serializer.validated_data['participants']))


class PrivateChatDetailView(RetrieveAPIView):
    serializer_class = PrivateChatSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return PrivateChat.objects.filter(participants=self.request.user)

class PrivateChatMessageListCreateView(ListCreateAPIView):
    serializer_class = PrivateChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_pk = self.kwargs['chat_pk']
        try:
            chat = PrivateChat.objects.get(pk=chat_pk, participants=self.request.user)
        except PrivateChat.DoesNotExist:
            self.queryset = PrivateChatMessage.objects.none()
            return self.queryset
        return chat.messages.all()


    def perform_create(self, serializer):
        chat_pk = self.kwargs['chat_pk']
        chat = PrivateChat.objects.get(pk=chat_pk)
        serializer.save(sender=self.request.user, chat=chat)
