from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile, Message
from django.shortcuts import get_object_or_404

from .serializers import MessageSerializer


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)
    return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
@require_POST
def register_view(request):
    data = json.loads(request.body)

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    birth_date = data.get('birth_date', None)

    if not username or not email or not password:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Email already exists'}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    profile = Profile.objects.create(user=user, birth_date=birth_date)
    return JsonResponse({'message': 'User registered successfully'})

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logout successful'}, status=200)
    return JsonResponse({'message': 'Method not allowed'}, status=405)



def password_reset_view(request):
    pass


class SendMessageView(APIView):
    def post(self, request):
        sender = request.user
        recipient_id = request.data.get('recipient')
        text = request.data.get('text')

        recipient = get_object_or_404(User, id=recipient_id)

        message = Message.objects.create(sender=sender, recipient=recipient, text=text)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReceivedMessagesView(APIView):
    def get(self, request):
        user = request.user
        received_messages = Message.objects.filter(recipient=user)
        serializer = MessageSerializer(received_messages, many=True)
        return Response(serializer.data)
