from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers

from .models import User


class CustomUserSerializer(UserSerializer):
    """Сериализатор для модели User."""

#    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name']


class CustomCreateUserSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""

    class Meta:
        model = User
        fields = ['email', "id", 'username', 'first_name', 'last_name', 'password']
