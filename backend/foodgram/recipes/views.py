from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ingredient, Tag, Recipe, RecipeFavorite, ShoppingCart
from .serializers import (IngredientSerializer, TagSerializer,
                          RecipeGetSerializer, RecipePostPatchDelSerializer,
                          FavoriteSerializer, ShoppingCartSerializer)


class RecipesViewSet(viewsets.ModelViewSet):
    """Рецепты."""

    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeGetSerializer

        return RecipePostPatchDelSerializer


class TagsViewSet(viewsets.ModelViewSet):
    """Теги."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientsViewSet(viewsets.ModelViewSet):
    """Ингредиенты."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = None
    #    filterset_fields = ('color', 'birth_year')
    search_fields = ('^name',)


class FavoriteView(APIView):
    """Избранное."""

    def post(self, request, id):

        user = request.user
        data = {
            'favorite_recipe': id,
            'user': user.id
        }

        if RecipeFavorite.objects.filter(
                favorite_recipe=id, user=user
        ).exists():
            raise ValidationError('Рецепт уже добавлен в избранное!')

        serializer = FavoriteSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):

        user = request.user

        if not RecipeFavorite.objects.filter(
                favorite_recipe=id, user=user
        ).exists():
            raise ValidationError(
                'Этот рецепт не входит в Ваш список избранного!'
            )

        subscribe = RecipeFavorite.objects.filter(
            favorite_recipe=id, user=user
        )
        subscribe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShopCartView(APIView):
    """Скачивание списка ингредиентов из рецепта, добавленного
    в список покупок."""




class ShoppingCartView(APIView):
    """Добавление и удаление рецепта в список покупок."""

    def post(self, request, id):

        user = request.user
        data = {
            'recipe_buy': id,
            'user': user.id
        }

        if ShoppingCart.objects.filter(recipe_buy=id, user=user).exists():
            raise ValidationError('Рецепт уже добавлен в список покупок!')

        serializer = ShoppingCartSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):

        user = request.user

        if not ShoppingCart.objects.filter(recipe_buy=id, user=user).exists():
            raise ValidationError(
                'Этот рецепт не входит в Ваш список покупок!'
            )

        subscribe = ShoppingCart.objects.filter(recipe_buy=id, user=user)
        subscribe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
