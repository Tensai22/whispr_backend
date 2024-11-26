from django.shortcuts import render
from .models import Message


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
