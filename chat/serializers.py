from rest_framework import serializers
from .models import ChatMessage, Group, GroupMembership, Community, CommunityMembership, Message

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username', read_only=True)
    sender_photo = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'sender_photo', 'text', 'timestamp']

    def get_sender_photo(self, obj):
        request = self.context.get('request')
        photo_url = obj.sender.profile.photo.url if obj.sender.profile.photo else '/media/profile_photos/default_profile_image.jpeg'
        return request.build_absolute_uri(photo_url) if request else photo_url


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


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

