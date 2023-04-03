from recipes.permissions import AuthorOrAdmin
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Subscription, User
from .serializers import SubscribeSerializer, SubscriptionsSerializer


class SubscriptionsView(ListAPIView):
    """Получение списка подписок пользователя на авторов."""

    permission_classes = (AuthorOrAdmin,)

    def get(self, request):
        user = request.user
        authors = User.objects.filter(subscribing__user=user)
        object = self.paginate_queryset(authors)
        serializer = SubscriptionsSerializer(
            object,
            many=True,
            context={'request': request}
        )

        return self.get_paginated_response(serializer.data)


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

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user

        if not Subscription.objects.filter(author=id, user=user).exists():
            raise ValidationError('Вы не подписаны на этого автора!')

        subscribe = Subscription.objects.filter(author=id, user=user)
        subscribe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
