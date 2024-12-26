# chat/consumers.py
import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, PrivateChatMessage, PrivateChat, Group
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
        self.user = await self.get_user_from_token()
        self.room_group_name = None  # Initialize room_group_name

        if self.user.is_authenticated:
            await self.accept()
            # Automatically join personal chat group
            await self.channel_layer.group_add(
                f"user_{self.user.id}",
                self.channel_name
            )
        else:
            await self.close(code=4001)

    async def disconnect(self, close_code):
        if self.room_group_name:
             await self.channel_layer.group_discard(
                    self.room_group_name,
                    self.channel_name
                )
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                f"user_{self.user.id}",
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data.get('message', '')
        chat_id = data.get('chatId')
        file_data = data.get('file')
        file_name = data.get('filename')

        if self.user.is_authenticated:
            if chat_id:
                try:
                     chat = await sync_to_async(PrivateChat.objects.get)(id=chat_id, participants__in=[self.user])
                     self.room_group_name = f"chat_{chat.id}"
                     await self.channel_layer.group_add(self.room_group_name, self.channel_name)

                     message = await sync_to_async(PrivateChatMessage.objects.create)(
                        sender=self.user,
                        chat=chat,
                        text=message_content
                     )
                     if file_data and file_name:
                         decoded_file = base64.b64decode(file_data)
                         message.file.save(f'private_chat_files/{file_name}', ContentFile(decoded_file), save=False)
                         await sync_to_async(message.save)()
                     user_data = await self.get_user_data(self.user)
                     print(f"Private message from user {self.user.username} (ID: {self.user.id}): {message_content} in chat {chat_id}")

                     await self.channel_layer.group_send(
                         self.room_group_name,
                         {
                             'type': 'chat_message',
                             'message': {
                                 'id': message.id,
                                 'user': user_data,
                                 'content': message.text,
                                 'timestamp': message.timestamp.isoformat(),
                                 'file': message.file.url if message.file else None,
                             }
                         }
                     )
                except PrivateChat.DoesNotExist:
                   try:
                         group = await sync_to_async(Group.objects.get)(id=chat_id, members__in=[self.user])
                         self.room_group_name = f"group_{group.id}"
                         await self.channel_layer.group_add(self.room_group_name, self.channel_name)

                         message = await sync_to_async(Message.objects.create)(
                             user=self.user,
                             content=message_content,
                             group=group
                         )
                         if file_data and file_name:
                             decoded_file = base64.b64decode(file_data)
                             message.file.save(f'chat_files/{file_name}', ContentFile(decoded_file), save=False)
                             await sync_to_async(message.save)()
                         user_data = await self.get_user_data(self.user)

                         print(f"Group message from user {self.user.username} (ID: {self.user.id}): {message_content} in group {group.id}")

                         await self.channel_layer.group_send(
                             self.room_group_name,
                             {
                                 'type': 'chat_message',
                                 'message': {
                                     'id': message.id,
                                     'user': user_data,
                                     'content': message.content,
                                     'timestamp': message.timestamp.isoformat(),
                                     'file': message.file.url if message.file else None,
                                 }
                             }
                         )
                   except Group.DoesNotExist:
                        print(f"Chat or group with id {chat_id} not found or user is not a participant")
            else:
                # Handle global messages (if needed, adjust group name)
                self.room_group_name = 'global_chat'  # Or any other global group name
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)

                message = await sync_to_async(Message.objects.create)(user=self.user, content=message_content)
                if file_data and file_name:
                    decoded_file = base64.b64decode(file_data)
                    message.file.save(f'chat_files/{file_name}', ContentFile(decoded_file), save=False)
                    await sync_to_async(message.save)()

                user_data = await self.get_user_data(self.user)

                message_data = {
                    'id': message.id,
                    'user': user_data,
                    'content': message.content,
                    'file': message.file.url if message.file else None,
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
    def get_user_data(self, user):
        try:
            profile = Profile.objects.get(user=user)
            avatar_url = profile.photo.url
        except Profile.DoesNotExist:
            avatar_url = None
        return {
           'id': user.id,
           'username': user.username,
           'avatar_url': avatar_url
        }