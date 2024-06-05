from rest_framework import serializers
from .models import ChatMessage
from logic.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    avatar = serializers.ImageField(source='user.avatar', read_only=True)
    class Meta:
        model = ChatMessage
        fields = ['user', 'content', 'timestamp']
