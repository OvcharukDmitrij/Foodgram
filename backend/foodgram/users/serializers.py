from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers

from recipes.models import Recipe
from .models import User, Subscription


class CustomUserSerializer(UserSerializer):
    """Получение пользователей."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj).exists()


class CustomCreateUserSerializer(UserCreateSerializer):
    """Создание пользователя."""

    class Meta:
        model = User
        fields = (
            'email', "id", 'username', 'first_name', 'last_name', 'password',
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор для получения рецептов в сериализаторе
    для получения подписок пользователя."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class SubscriptionsSerializer(serializers.ModelSerializer):
    """Получение подписок пользователя."""

    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj).exists()

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        if not recipes:
            return False
        return RecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class SubscribeSerializer(serializers.ModelSerializer):
    """Создание подписки пользователя на автора."""

    class Meta:
        model = Subscription
        fields = ('user', 'author',)

    def to_representation(self, instance):
        return SubscriptionsSerializer(
            instance.author,
            context={'request': self.context.get('request')}
        ).data
