
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


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
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirmPassword')

        if password != confirm_password:
            return JsonResponse({'message': 'Passwords do not match'}, status=400)

        if User.objects.filter(username=email).exists():
            return JsonResponse({'message': 'User already exists'}, status=400)

        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()
        return JsonResponse({'message': 'User registered successfully'}, status=201)
    return JsonResponse({'message': 'Method not allowed'}, status=405)