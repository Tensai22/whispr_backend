# consumers.py
import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Используем глобальный канал
        self.room_group_name = 'chat_global'

        # Присоединение к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Удаление из группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

        # Сохранение сообщения в базе данных
        await sync_to_async(Message.objects.create)(
            message=message
        )

        # Отправка сообщения в группу
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Отправка сообщения всем подключенным клиентам
        await self.send(text_data=json.dumps({
            'message': message
        }))
