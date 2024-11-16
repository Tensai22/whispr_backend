from rest_framework import serializers
from .models import User, Profile, ChatMessage, Group, GroupMembership


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['photo', 'birth_date', 'last_activity']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data, profile=None):
        profile_data = validated_data.pop(profile, {})
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.photo = profile_data.get('photo', instance.photo)
        profile.birth_date = profile_data.get('birth_date', instance.birth_date)
        profile.save()

        return instance


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
