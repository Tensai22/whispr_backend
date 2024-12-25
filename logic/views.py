from django.db.models import Q
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Profile
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from django.http import JsonResponse
import json
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['username'] = user.username
        return data


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response(
                {'message': 'User registered successfully', 'access': tokens['access'], 'refresh': tokens['refresh']},
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileUpdateView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def password_change_view(request):
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



@api_view(['POST'])
@permission_classes([AllowAny])
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


@api_view(['POST'])
@permission_classes([AllowAny])
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
        return JsonResponse({'message': 'Password has been reset successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid reset link'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_avatar(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if 'avatar' in request.FILES:
        profile.photo = request.FILES['avatar']
        profile.save()

        return Response({
            'avatar_url': profile.photo.url
        }, status=200)

    return Response({'error': 'No avatar file provided'}, status=400)


def profile_view(request, id):
    user = get_object_or_404(User, id=id)
    profile = get_object_or_404(Profile, user=user)
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'birth_date': profile.birth_date,
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

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
def get_users_with_messages(request):
    # Получаем текущего пользователя
    user = request.user

    # Ищем всех пользователей, с которыми был обмен сообщениями
    users = User.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).distinct()

    # Сериализация данных
    users_json = serializers.serialize('json', users, fields=('id', 'username'))
    users_data = json.loads(users_json)

    # Формируем список пользователей
    users_list = [{"id": user['pk'], "username": user['fields']['username']} for user in users_data]

    return JsonResponse(users_list, safe=False)