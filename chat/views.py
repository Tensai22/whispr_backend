import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Message, ChatMessage, Group, GroupMembership, Chat, CommunityMembership, Community
from .serializers import ChatMessageSerializer, CommunitySerializer, CommunityMembershipSerializer, GroupSerializer, GroupMembershipSerializer


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


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Message

class GetMessagesView(APIView):
    def get(self, request):
        messages = Message.objects.all().order_by('-timestamp')
        data = [{'id': msg.id, 'text': msg.message, 'timestamp': msg.timestamp} for msg in messages]
        return Response({'messages': data})

@csrf_exempt
@require_GET
def get_messages(request):
    try:
        messages = ChatMessage.objects.all().order_by('-timestamp')
        serializer = ChatMessageSerializer(messages, many=True, context={'request': request})
        return JsonResponse({'messages': serializer.data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def send_message(request):
    try:
        data = json.loads(request.body)
        text = data.get('text')
        if not text:
            return JsonResponse({'error': 'No message text provided'}, status=400)

        message = ChatMessage.objects.create(sender=request.user, text=text)
        message_data = {'id': message.id, 'sender': message.sender.username, 'text': message.text,
                        'timestamp': message.timestamp}
        return JsonResponse(message_data, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

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