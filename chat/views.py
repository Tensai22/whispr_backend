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