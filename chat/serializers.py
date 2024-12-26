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
    photo = serializers.ImageField(required=False)
    user_role = serializers.SerializerMethodField()
    moderators = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'photo', 'admin', 'members', 'created_at', 'user_role', 'moderators']
        #бета тест
        read_only_fields = ['moderators']

    def get_moderators(self, obj):  # Добавляем метод для получения модераторов
        moderators = CommunityMembership.objects.filter(community=obj, role='moderator')
        return [
            {
                'id': membership.user.id,
                'username': membership.user.username,
            }
            for membership in moderators
        ]

    def get_user_role(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                membership = CommunityMembership.objects.get(user=request.user, community=obj)
                return membership.role
            except CommunityMembership.DoesNotExist:
                return None
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_id = self.context['request'].user.id

        # Добавляем информацию о роли пользователя в сообществе
        try:
            membership = CommunityMembership.objects.get(user_id=user_id, community=instance)
            representation['user_role'] = membership.role
        except CommunityMembership.DoesNotExist:
            representation['user_role'] = None

        # Добавляем данные админа
        if instance.admin:
            representation['admin'] = {
                'id': instance.admin.id,
                'username': instance.admin.username,
            }

        # Добавляем данные модераторов
        '''
        moderators = CommunityMembership.objects.filter(community=instance, role='moderator')
        representation['moderators'] = [
            {
                'id': membership.user.id,
                'username': membership.user.username,
            }
            for membership in moderators
        ]'''
        representation['moderators'] = self.get_moderators(instance)

        return representation

class CommunityMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CommunityMembership
        fields = ['id', 'user', 'community', 'role', 'join_date']
        read_only_fields = ['user']

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
            return None
class MessageSerializer(serializers.ModelSerializer):
    user = MessageUserSerializer(read_only=True)
    file = serializers.FileField(required=False)
    class Meta:
        model = Message
        fields = ['id', 'user', 'content', 'timestamp', 'file']

class PrivateChatSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    messages = serializers.SerializerMethodField()

    class Meta:
        model = PrivateChat
        fields = ['id', 'participants', 'created_at', 'messages']
        read_only_fields = ['created_at']

    def get_messages(self, obj):
          messages = obj.messages.all().order_by('timestamp')
          return PrivateChatMessageSerializer(messages, many=True).data

class PrivateChatMessageSerializer(serializers.ModelSerializer):
    user = MessageUserSerializer(source='sender', read_only=True)
    content = serializers.CharField(source='text')
    file = serializers.FileField(required=False)

    class Meta:
        model = PrivateChatMessage
        fields = ['id', 'user', 'content', 'timestamp', 'file']

    def get_user(self, obj):
        try:
            profile = Profile.objects.get(user=obj.sender)
            avatar_url = profile.photo.url
        except Profile.DoesNotExist:
            avatar_url = None
        return {
            'id': obj.sender.id,
            'username': obj.sender.username,
            'avatar_url': avatar_url,
        }