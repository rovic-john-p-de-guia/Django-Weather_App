from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.password_validation import validate_password
from django.core.files.images import get_image_dimensions

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['photo']

class RegisterSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'photo']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_photo(self, value):
        if value:
            if value.size > 2 * 1024 * 1024:
                raise serializers.ValidationError('Image size should not exceed 2MB.')
            if not value.content_type in ['image/jpeg', 'image/png', 'image/webp']:
                raise serializers.ValidationError('Only JPEG, PNG, and WebP images are allowed.')
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords do not match.')
        return data

    def create(self, validated_data):
        photo = validated_data.pop('photo', None)
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        if photo:
            UserProfile.objects.create(user=user, photo=photo)
        else:
            UserProfile.objects.create(user=user)
        user.set_password(password)
        user.save()
        return user 