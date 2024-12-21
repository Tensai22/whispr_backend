from rest_framework import serializers

from logic.serializers import UserSerializer
from .models import Group, GroupMembership, Community, CommunityMembership, Message, PrivateChatMessage, PrivateChat
from logic.models import User, Profile

class GroupSerializer(serializers.ModelSerializer):
    admin = serializers.StringRelatedField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'
class GroupMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMembership
        fields = ['user', 'group', 'role', 'join_date']

class CommunitySerializer(serializers.ModelSerializer):
    admin = serializers.StringRelatedField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Community
        fields = '__all__'


class CommunityMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityMembership
        fields = ['user', 'community', 'join_date']


class MessageUserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar_url']

    def get_avatar_url(self, obj):
        try:
            profile = Profile.objects.get(user=obj)
            return profile.photo.url
        except Profile.DoesNotExist:
            return None # Или URL стандартной аватарки

class MessageSerializer(serializers.ModelSerializer):
    user = MessageUserSerializer(read_only=True) # Используйте MessageUserSerializer

    class Meta:
        model = Message
        fields = ['id', 'user', 'content', 'timestamp']

class PrivateChatSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = PrivateChat
        fields = ['id', 'participants', 'created_at', 'messages']
        read_only_fields = ['created_at']


class PrivateChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.name', read_only=True)

    class Meta:
        model = PrivateChatMessage
        fields = ['id', 'sender', 'text', 'timestamp']

