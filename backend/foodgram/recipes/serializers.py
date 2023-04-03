import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from users.serializers import CustomUserSerializer

from .models import (Ingredient, Recipe, RecipeFavorite, RecipeIngredient,
                     RecipeTag, ShoppingCart, Tag)


class RecipeIngredientGetSerializer(serializers.ModelSerializer):
    """Получение данных об ингредиентах и их количестве в рецепте."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeIngredientPostSerializer(serializers.ModelSerializer):
    """Добавление ингредиентов и их количество при создании рецепта."""

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount',)


class IngredientSerializer(serializers.ModelSerializer):
    """Получение данных об ингредиентах."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class TagSerializer(serializers.ModelSerializer):
    """Получение данных о тегах."""

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class Base64ImageField(serializers.ImageField):
    """Декодирование картинки рецепта."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeGetSerializer(serializers.ModelSerializer):
    """Получение рецептов."""

    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_ingredients(self, obj):

        ingredients = RecipeIngredient.objects.filter(recipe=obj)

        return RecipeIngredientGetSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):

        request = self.context.get('request')

        if request is None or request.user.is_anonymous:
            return False

        return RecipeFavorite.objects.filter(
            favorite_recipe=obj, user=request.user
        ).exists()

    def get_is_in_shopping_cart(self, obj):

        request = self.context.get('request')

        if request is None or request.user.is_anonymous:
            return False

        return ShoppingCart.objects.filter(
            recipe_buy=obj, user=request.user
        ).exists()


class RecipePostPatchDelSerializer(serializers.ModelSerializer):
    """Создание, изменение и удаление рецептов."""

    ingredients = RecipeIngredientPostSerializer(
        source='recipeingredient',
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'author', 'image', 'text',
            'ingredients', 'tags', 'cooking_time',
        )

    def create(self, validated_data):

        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipeingredient')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)

        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(id=ingredient['id'])
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=ingredient['amount'],
            )

        for tag in tags:
            RecipeTag.objects.create(tag=tag, recipe=recipe)

        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        RecipeIngredient.objects.filter(recipe=instance).delete()
        RecipeTag.objects.filter(recipe=instance).delete()
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipeingredient')
        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(id=ingredient['id'])
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=instance,
                amount=ingredient['amount']
            )
        for tag in tags:
            RecipeTag.objects.create(tag=tag, recipe=instance)

        return instance

    def to_representation(self, instance):
        return RecipeGetSerializer(instance).data


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор для сериализатора FavoriteSerializer."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class FavoriteSerializer(serializers.ModelSerializer):
    """Добавление пользователем рецепта в избранное."""

    class Meta:
        model = RecipeFavorite
        fields = ('user', 'favorite_recipe',)

    def to_representation(self, instance):
        return RecipeFavoriteSerializer(instance.favorite_recipe).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Добавление пользователем рецепта в список покупок."""

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe_buy',)

    def to_representation(self, instance):
        return RecipeFavoriteSerializer(instance.recipe_buy).data
