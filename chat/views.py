# chat/views.py
import json
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveAPIView, \
    CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Message, Group, GroupMembership, Chat, CommunityMembership, Community, PrivateChat, \
    PrivateChatMessage
from .serializers import CommunitySerializer, CommunityMembershipSerializer, GroupSerializer, \
    GroupMembershipSerializer, MessageSerializer, PrivateChatSerializer, PrivateChatMessageSerializer
from .serializers import CommunitySerializer, CommunityMembershipSerializer, GroupSerializer, \
    GroupMembershipSerializer, MessageSerializer, PrivateChatSerializer, PrivateChatMessageSerializer
from logic.models import User
from logic.serializers import UserSerializer

import logging

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

    def perform_create(self, serializer):
         group = serializer.save(admin=self.request.user)
         GroupMembership.objects.create(user=self.request.user, group=group, role='admin')


class GroupDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

class GroupMembershipListView(ListCreateAPIView):
    queryset = GroupMembership.objects.all()
    serializer_class = GroupMembershipSerializer
    permission_classes = [IsAuthenticated]


class CommunityListView(ListAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]
'''
class CommunityCreateView(ListCreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]'''

class CommunityCreateView(generics.CreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        community = serializer.save(admin=self.request.user)
        CommunityMembership.objects.create(user=self.request.user, community=community, role='admin')

class CommunityDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_object(self):
        obj = super().get_object()
        # Добавляем информацию о роли пользователя в сообществе
        try:
            membership = CommunityMembership.objects.get(user=self.request.user, community=obj)
            obj.user_role = membership.role
        except CommunityMembership.DoesNotExist:
            obj.user_role = None
        return obj

class CommunityMembershipListView(ListAPIView):
    queryset = CommunityMembership.objects.all()
    serializer_class = CommunityMembershipSerializer
    permission_classes = [IsAuthenticated]

logger = logging.getLogger(__name__)

class CommunityJoinView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        logger.info(f"Join request: user={request.user}, community_id={pk}, data={request.data}")  # Логируем запрос
        try:
            community = Community.objects.get(pk=pk)
            if not CommunityMembership.objects.filter(user=request.user, community=community).exists():
                CommunityMembership.objects.create(user=request.user, community=community, role='member')
                logger.info(f"User {request.user} joined community {pk}") # Логируем успешное вступление
                return Response({'message': 'Вы успешно подписались на сообщество'}, status=status.HTTP_200_OK)
            logger.info(f"User {request.user} is already a member of community {pk}") # Логируем если уже участник
            return Response({'message': 'Вы уже являетесь участником этого сообщества'}, status=status.HTTP_400_BAD_REQUEST)
        except Community.DoesNotExist:
            logger.error(f"Community with id {pk} not found") # Логируем ошибку
            return Response({'error': 'Сообщество не найдено'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error joining community: {e}, data: {request.data}") # Логируем ошибку
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CommunityLeaveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            community = Community.objects.get(pk=pk)
            membership = CommunityMembership.objects.filter(user=request.user, community=community)
            if membership.exists():
                membership.delete()
                return Response({'message': 'Вы успешно отписались от сообщества'}, status=status.HTTP_200_OK)
            return Response({'message': 'Вы не являетесь участником этого сообщества'}, status=status.HTTP_400_BAD_REQUEST)
        except Community.DoesNotExist:
            return Response({'error': 'Сообщество не найдено'}, status=status.HTTP_404_NOT_FOUND)

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

class CommunitySearchView(generics.ListAPIView):
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Community.objects.filter(name__icontains=query)


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

        messages = chat.messages.all().order_by('timestamp')
        return messages

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

class UserCommunitiesListView(generics.ListAPIView):
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Community.objects.filter(members=user)


class UserGroupsListView(generics.ListAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Group.objects.filter(members=user)

class GroupMessagesView(ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        group_pk = self.kwargs['pk']
        try:
          group = Group.objects.get(pk=group_pk, members=self.request.user)
        except Group.DoesNotExist:
            return Message.objects.none()
        messages = group.group_messages.all().order_by('timestamp')
        return messages
    def perform_create(self, serializer):
        group_pk = self.kwargs['pk']
        try:
            group = Group.objects.get(pk=group_pk, members__in=[self.request.user])
        except Group.DoesNotExist:
            return
        serializer.save(user=self.request.user, group=group)

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == request.user:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({
                'id': instance.id,
                'username': instance.username,
                'profile_photo': instance.profile.photo.url if instance.profile.photo else None
            })
