import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Message
from logic.models import Profile
from channels.db import database_sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs
import base64
from django.core.files.base import ContentFile
import os
from django.conf import settings

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
        message_content = data.get('message', '')
        file_data = data.get('file')
        file_name = data.get('filename')

        user = await self.get_user_from_token()

        if user.is_authenticated:
            message = await self.save_message(user, message_content, file_data, file_name)

            try:
                profile = await sync_to_async(Profile.objects.get)(user=user)
                avatar_url = profile.photo.url
            except Profile.DoesNotExist:
                avatar_url = None

            message_data = {
                'id': message.id,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'avatar_url': avatar_url,
                },
                'content': message.content,
                'file': message.file.name if message.file else None,
                'timestamp': message.timestamp.isoformat()
            }

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_data
                }
            )
        else:
            print('User is not authenticated, message not sent.')

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def get_user_from_token(self):
        token = self.scope['query_string'].decode().split('=')[1] if self.scope['query_string'] else None
        if token:
            jwt_auth = JWTAuthentication()
            try:
                validated_token = jwt_auth.get_validated_token(token)
                user = jwt_auth.get_user(validated_token)
                return user
            except:
                return AnonymousUser()
        return AnonymousUser()

    @database_sync_to_async
    def save_message(self, user, message_content, file_data, file_name):
        message = Message.objects.create(user=user, content=message_content)

        if file_data and file_name:
            # Убрано: file_path = os.path.join(settings.MEDIA_ROOT, 'chat_files', file_name)
            decoded_file = base64.b64decode(file_data)

            # Изменено: сохраняем файл с указанием относительного пути
            message.file.save('chat_files/' + file_name, ContentFile(decoded_file), save=False)
            message.save()

            # Отладочный вывод
            print("File saved to:", message.file.path)
            print("message.file.name:", message.file.name)

        return message