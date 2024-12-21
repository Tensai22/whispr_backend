from rest_framework import serializers
from .models import User, Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['photo', 'birth_date', 'last_activity']


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar_url']  # Добавьте avatar_url

    def get_avatar_url(self, obj):
        try:
            profile = Profile.objects.get(user=obj)
            return profile.photo.url
        except Profile.DoesNotExist:
            return None # Или URL стандартной аватарки

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
