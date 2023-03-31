from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Subscription
from .serializers import SubscribeSerializer, SubscriptionsSerializer


class SubscriptionsView(APIView):
    """Получение списка подписок пользователя на авторов."""


    def get(self, request):
        user = request.user
        authors = User.objects.filter(subscribing__user=user)
        serializer = SubscriptionsSerializer(
            authors,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)


class SubscribeView(APIView):
    """Создание и удаление подписки пользователя на автора."""

    def post(self, request, id):
        user = request.user
        data = {
            'author': id,
            'user': user.id
        }

        if id == user.id:
            raise ValidationError('Нельзя подписаться на себя!')
        if Subscription.objects.filter(author=id, user=user).exists():
            raise ValidationError('Вы уже подписаны на этого автора!')

        serializer = SubscribeSerializer(
            data=data,
            context={'request': request}
        )

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
