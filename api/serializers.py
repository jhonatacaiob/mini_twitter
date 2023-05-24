from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password')
        )
        return super(UserSerializer, self).create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    posted_at = serializers.DateTimeField(source='created_at')

    class Meta:
        model = Post
        fields = [
            'content',
            'user',
            'posted_at',
        ]
