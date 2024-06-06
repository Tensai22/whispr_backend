from rest_framework import serializers
from .models import User, Profile, ChatMessage


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

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'text', 'timestamp']