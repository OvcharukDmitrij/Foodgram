from rest_framework import serializers

from .models import User


class LoginSerializer(serializers.Serializer):
    """Сериализатор выдачи токена новому пользователю."""

    password = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=254, required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с указанной почтой не зарегистрирован!')

        return email


class SetPasswordSerializer(serializers.Serializer):
    """Сериализатор выдачи токена новому пользователю."""

    new_password = serializers.CharField(max_length=150, required=True)
    current_password = serializers.CharField(max_length=254, required=True)


class UserGetSerializer(serializers.ModelSerializer):
    """Сериализатор модели User для работы со списком пользователей,
     конкретным пользователем и самим собой."""

    is_subscribed = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User для создания нового пользователя."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password')
