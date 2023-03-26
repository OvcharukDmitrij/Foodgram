from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets

from .models import Ingredient, Tag, Recipe
from .serializers import IngredientSerializer, TagSerializer, RecipeGetSerializer, RecipePostPatchDelSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeGetSerializer

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeGetSerializer

        return RecipePostPatchDelSerializer


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = None
    #    filterset_fields = ('color', 'birth_year')
    search_fields = ('^name',)


class FavoritViewSet:
    pass


class ShopCartViewSet:
    pass
