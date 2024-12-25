from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['photo', 'birth_date']

class AvatarUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['photo']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data.pop('profile', None)
        user = User.objects.create_user(**validated_data)
        return user
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        if 'password' in validated_data:
            instance.set_password(validated_data.get('password'))

        instance.save()

        profile = instance.profile
        if profile_data:
            profile.photo = profile_data.get('photo', profile.photo)
            profile.birth_date = profile_data.get('birth_date', profile.birth_date)
            profile.save()

        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    birth_date = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar_url', 'birth_date']

    def get_avatar_url(self, obj):
        try:
            profile = Profile.objects.get(user=obj)
            return profile.photo.url
        except Profile.DoesNotExist:
            return None

    def get_birth_date(self, obj):
        try:
            profile = Profile.objects.get(user=obj)
            return profile.birth_date
        except Profile.DoesNotExist:
            return None