from django.db.models import Sum
from django.http import HttpResponse
from django_filters import rest_framework as f
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import RecipeFilter
from .models import (Ingredient, Recipe, RecipeFavorite, RecipeIngredient,
                     ShoppingCart, Tag)
from .permissions import AuthorOrAdmin
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeGetSerializer, RecipePostPatchDelSerializer,
                          ShoppingCartSerializer, TagSerializer)


class RecipesViewSet(viewsets.ModelViewSet):
    """Рецепты."""

    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrAdmin,)
    filter_backends = (f.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeGetSerializer

        return RecipePostPatchDelSerializer

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list':
            return AllowAny(),
        return super().get_permissions()

    @action(
        detail=False,
        methods=['get'],
        serializer_class=RecipeGetSerializer,
    )
    def download_shopping_cart(self, request):
        """Загрузка списка покупок."""

        ingredient_list = "Ингредиенты для покупки: "

        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
            amount=Sum('amount')
        )

        for ingredient in ingredients:
            ingredient_list += (
                f"\n{ingredient['ingredient__name']}"
                f"({ingredient['ingredient__measurement_unit']}) - "
                f"{ingredient['amount']}")

        return HttpResponse(ingredient_list, content_type='application')


class TagsViewSet(viewsets.ModelViewSet):
    """Теги."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


class IngredientsViewSet(viewsets.ModelViewSet):
    """Ингредиенты."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (AllowAny,)
    pagination_class = None
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

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

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

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):

        user = request.user

        if not ShoppingCart.objects.filter(recipe_buy=id, user=user).exists():
            raise ValidationError(
                'Этот рецепт не входит в Ваш список покупок!'
            )

        subscribe = ShoppingCart.objects.filter(recipe_buy=id, user=user)
        subscribe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
