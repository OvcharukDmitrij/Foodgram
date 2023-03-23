from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets

from .models import Ingredient, Tag
from .serializers import IngredientSerializer, TagSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    pass


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
