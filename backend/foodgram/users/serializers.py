import re

from rest_framework import serializers, status
from .models import User
from .utils import CustomValidation


class LoginSerializer(serializers.Serializer):
    """Сериализатор выдачи токена новому пользователю"""

    password = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=254, required=True)

    # def validate_email(self, email):
    #     if not User.objects.filter(email=email).exists():
    #         return serializers.ValidationError(
    #             'Пользователь с указанным email не зарегистрирован!'
    #         )
    #
    # def validate_password(self, password):
    #     if not User.objects.filter(password=password).exists():
    #         return serializers.ValidationError(
    #             'Пользователь с указанным паролем не зарегистрирован!'
    #         )

class SetPasswordSerializer(serializers.ModelSerializer):
    """Сериализатор изменения пароля."""

    new_password = serializers.CharField(max_length=150, required=True)
    current_password = serializers.CharField(max_length=150, required=True)


    class Meta:
        model = User
        fields = ('current_password', 'new_password')


# class TokenSerializer(serializers.Serializer):
#     """Сериализатор выдачи токена пользователю."""
#
#     username = serializers.CharField(max_length=150, required=True)
#     confirm_code = serializers.UUIDField(required=True)
#
#     def validate_username(self, username):
#         if re.match(r'me', username):
#             return serializers.ValidationError(
#                 'Недопустимое имя пользователя!'
#             )
#
#         if not User.objects.filter(username=username).exists():
#             raise CustomValidation(
#                 'Данный пользователь не зарегистрирован.',
#                 'username',
#                 status_code=status.HTTP_404_NOT_FOUND)
#
#         if not re.match(r'^[a-zA-Z0-9]+$', username):
#             raise serializers.ValidationError('Недопустимые символы username')
#
#         return username
#
#     def validate_confirm_code(self, confirm_code):
#         if not User.objects.filter(confirm_code=confirm_code).exists():
#             raise serializers.ValidationError('Данный confirm_code нет в БД.')
#
#         return confirm_code
#
#     def validate(self, data):
#         if not User.objects.filter(
#                 confirm_code=data['confirm_code'],
#                 username=data['username']
#         ).exists():
#             raise serializers.ValidationError(
#                 'Данная пара username + confirm_code не зарегистрирована.'
#             )
#
#         return data

class UserGetSerializer(serializers.ModelSerializer):
    """Сериализатор модели User для работы со списком пользователей,
     конкретным пользователем и самим собой."""

    is_subscribed = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User для создания нового пользователя """

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password')
