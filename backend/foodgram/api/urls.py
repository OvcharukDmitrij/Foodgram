from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import a
    # RecipesViewSet, TagsViewSet, IngredientsViewSet,
    #                 FavoritViewSet, ShopCartViewSet

#router_v1 = DefaultRouter()

#router_v1.register(r'recipes', RecipesViewSet)
# router_v1.register(r'tags', TagsViewSet, basename='favori')
# router_v1.register(r'ingredients', IngredientsViewSet, basename='favor')
# router_v1.register(r'recipes/(?P<post_id>\d+)/favorite', FavoritViewSet,
#                    basename='favorits')
# router_v1.register(r'recipes/download_shopping_cart', ShopCartViewSet, basename='favo')


urlpatterns = [
    #path('', include(router_v1.urls)),
    path('', a)
]
