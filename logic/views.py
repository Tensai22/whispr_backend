from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import Profile

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, username=email, password=password)
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