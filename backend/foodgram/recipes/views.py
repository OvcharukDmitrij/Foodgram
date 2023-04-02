from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (Ingredient, Tag, Recipe, RecipeFavorite,
                     ShoppingCart, RecipeIngredient)
from .serializers import (IngredientSerializer, TagSerializer,
                          RecipeGetSerializer, RecipePostPatchDelSerializer,
                          FavoriteSerializer, ShoppingCartSerializer)
from .permissions import AuthorOrAdmin

class RecipesViewSet(viewsets.ModelViewSet):
    """Рецепты."""

    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tags',)
    ordering_fields = ('-pub_date',)

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

        user = request.user
        ingredient_list = "Cписок покупок: "

        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=user).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
            amount=Sum('amount'))

        for num, i in enumerate(ingredients):
            ingredient_list += (
                f"\n{i['ingredient__name']} - {i['amount']} "
                f"{i['ingredient__measurement_unit']}"
            )
            if num < ingredients.count() - 1:
                ingredient_list += ', '

        response = HttpResponse(
            ingredient_list, 'Content-Type: application/pdf'
        )
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.pdf'
        )
        return response


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
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    permission_classes = (AllowAny,)
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
