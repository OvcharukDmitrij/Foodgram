from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Subscription
from .serializers import (CustomUserSerializer, SubscriptionsSerializer,
                          SubscribeSerializer)


class CustomUserViewSet(UserViewSet):
    """Получение списка пользователей, конкретного пользователя
    и регистрация пользователя."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class SubscriptionsViewSet(viewsets.ModelViewSet):
    """Получение перечня подписок пользователя на авторов."""

    queryset = User.objects.all()
    serializer_class = SubscriptionsSerializer


class SubscribeView(APIView):
    """Создание и удаление подписки пользователя на автора."""

    def post(self, request, id):
        user = request.user
        data = {
            'author': id,
            'user': user.id
        }

        if id == user:
            raise ValidationError('Нельзя подписаться на себя!')
        if Subscription.objects.filter(author=id, user=user).exists():
            raise ValidationError('Вы уже подписаны на этого автора!')

        serializer = SubscribeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = request.user

        if not Subscription.objects.filter(author=id, user=user).exists():
            raise ValidationError('Вы не подписаны на этого автора!')

        subscribe = Subscription.objects.filter(author=id, user=user)
        subscribe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
