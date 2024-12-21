import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from logic.models import Profile  # Импортируйте модель Profile

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'global_chat'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data['message']
        user = self.scope['user'] # Получаем пользователя из scope

        if user.is_authenticated:
            message = await sync_to_async(Message.objects.create)(
                user=user,
                content=message_content
            )

            # Получаем профиль пользователя
            try:
                profile = await sync_to_async(Profile.objects.get)(user=user)
                avatar_url = profile.photo.url
            except Profile.DoesNotExist:
                # Обработка случая, когда профиль не создан (маловероятно, но возможно)
                avatar_url = None

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': {
                        'id': message.id,
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'avatar_url': avatar_url,  # Добавляем URL аватара
                        },
                        'content': message.content,
                        'timestamp': message.timestamp.isoformat()
                    }
                }
            )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))