from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatMessage

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        user = request.user
        message = request.POST.get('message')
        if message:
            ChatMessage.objects.create(user=user, message=message)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
    elif request.method == 'GET':
        messages = ChatMessage.objects.all().order_by('-timestamp')[:50]  # Retrieve last 50 messages
        data = [{'user': msg.user.username, 'message': msg.message, 'timestamp': msg.timestamp} for msg in messages]
        return JsonResponse(data, safe=False)
