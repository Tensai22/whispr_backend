import json
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile, ChatMessage
from .serializers import UserSerializer, ChatMessageSerializer
from django.core import serializers


@csrf_exempt
@require_POST
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
    try:
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
        Profile.objects.create(user=user, birth_date=birth_date)
        return JsonResponse({'message': 'User registered successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def send_message(request):
    try:
        data = json.loads(request.body)
        user = request.user
        text = data.get('text')

        if not user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        if not text:
            return JsonResponse({'error': 'Message text is required'}, status=400)

        chat_message = ChatMessage.objects.create(sender=user, text=text)
        return JsonResponse(ChatMessageSerializer(chat_message).data, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_GET
def get_messages(request):
    try:
        messages = ChatMessage.objects.all().order_by('-timestamp')
        serialized_messages = ChatMessageSerializer(messages, many=True).data
        return JsonResponse({'messages': serialized_messages}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



class profile_update_view(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

@csrf_exempt
@require_POST
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logout successful'}, status=200)
    return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
@login_required
@require_POST
def password_change_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        if not old_password or not new_password or not confirm_new_password:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        if new_password != confirm_new_password:
            return JsonResponse({'error': 'New passwords do not match'}, status=400)

        user = request.user
        if not user.check_password(old_password):
            return JsonResponse({'error': 'Old password is incorrect'}, status=400)

        user.set_password(new_password)
        user.save()
        return JsonResponse({'message': 'Password change confirmed'}, status=200)

    return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
@require_POST
def password_reset_view(request):
    data = json.loads(request.body)
    email = data.get('email')

    if not email:
        return JsonResponse({'error': 'Email is required'}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User with this email does not exist'}, status=400)

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f'http://localhost:3000/reset/{uid}/{token}'

    subject = 'Password Reset Request'
    message = render_to_string('password_reset_email.html', {'user': user, 'reset_link': reset_link})

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

    return JsonResponse({'message': 'Password reset link has been sent to your email'}, status=200)

@csrf_exempt
@require_POST
def password_reset_confirm_view(request, uidb64, token):
    data = json.loads(request.body)
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    if not new_password or not confirm_password:
        return JsonResponse({'error': 'New password and confirmation are required'}, status=400)

    if new_password != confirm_password:
        return JsonResponse({'error': 'Passwords do not match'}, status=400)

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.set_password(new_password)
        user.save()
        send_mail()
        return JsonResponse({'message': 'Password has been reset successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid reset link'}, status=400)





def profile_view(request, id):
    user = get_object_or_404(User, id=id)
    profile = get_object_or_404(Profile, user=user)
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'birth_date': profile.birth_date,
        'last_activity': profile.last_activity,
    }
    return JsonResponse(user_data, status=200)


@csrf_exempt
def search_users(request):
    query = request.GET.get('q', '')
    if query:
        users = User.objects.filter(username__icontains=query)
        users_json = serializers.serialize('json', users, fields=('id', 'username'))
        users_data = json.loads(users_json)
        users_list = [{"id": user['pk'], "username": user['fields']['username']} for user in users_data]
        return JsonResponse(users_list, safe=False)
    return JsonResponse([], safe=False)

