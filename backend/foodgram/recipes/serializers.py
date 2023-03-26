from rest_framework import serializers
import base64
from django.core.files.base import ContentFile
from users.serializers import CustomUserSerializer


from .models import Ingredient, Tag, Recipe, RecipeTag, RecipeIngredient


class RecipeIngredientGetSerializer(serializers.ModelSerializer):
    """Сериализатор для предоставления данных об ингредиентах и их количества
    в рецепте."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeIngredientPostSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления ингредиентов и их количества при
     создании рецепта."""

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount',)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для предоставления данных об ингредиентах."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для предоставления данных о тегах."""

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class Base64ImageField(serializers.ImageField):
    """Сериализатор для декодирования картинки рецепта."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор получения рецептов."""

#    ingredients = RecipeIngredientSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time'
        )

    def get_ingredients(self, obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientGetSerializer(ingredients, many=True).data


class RecipePostPatchDelSerializer(serializers.ModelSerializer):
    """Сериализатор для создания, изменения и удаления рецептов."""

    ingredients = RecipeIngredientPostSerializer(source='recipeingredient', many=True)
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
        print(validated_data)

        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipeingredient')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)
        for ingredient in ingredients:
            current_ingredient, status = Ingredient.objects.get_or_create(
                id=ingredient['id']
            )
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=ingredient['amount']
            )
        for tag in tags:
            RecipeTag.objects.create(tag=tag, recipe=recipe)

        return recipe