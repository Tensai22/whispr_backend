import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Message, Group, GroupMembership, Chat, CommunityMembership, Community, PrivateChat, \
    PrivateChatMessage
from .serializers import CommunitySerializer, CommunityMembershipSerializer, GroupSerializer, \
    GroupMembershipSerializer, MessageSerializer, PrivateChatSerializer, PrivateChatMessageSerializer


def index(request):
    return render(request, 'chat/index.html')

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
        participants = serializer.validated_data.get('participants', [])
        if self.request.user not in participants:
            participants.append(self.request.user)
        serializer.save(participants=participants)


class PrivateChatDetailView(RetrieveAPIView):
    serializer_class = PrivateChatSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return PrivateChat.objects.filter(participants=self.request.user)


class PrivateChatMessagesView(ListCreateAPIView):
    serializer_class = PrivateChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_pk = self.kwargs['pk']
        try:
            chat = PrivateChat.objects.get(pk=chat_pk, participants=self.request.user)
        except PrivateChat.DoesNotExist:
            return PrivateChatMessage.objects.none()
        return chat.messages.all().order_by('timestamp')

    def perform_create(self, serializer):
        chat_pk = self.kwargs['pk']
        try:
             chat = PrivateChat.objects.get(pk=chat_pk, participants__in=[self.request.user])
        except PrivateChat.DoesNotExist:
           participants = [self.request.user] + serializer.validated_data.get('participants', [])

           chat = PrivateChat.objects.create(
             participants=participants
           )
        serializer.save(sender=self.request.user, chat=chat)