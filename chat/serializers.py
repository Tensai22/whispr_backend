from rest_framework import serializers
from .models import Message
from logic.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    avatar = serializers.ImageField(source='user.avatar', read_only=True)
    class Meta:
        model = Message
        fields = ['user', 'content', 'timestamp']
