from django.urls import include, path
from recipes.views import (FavoriteView, IngredientsViewSet, RecipesViewSet,
                           ShoppingCartView, TagsViewSet)
from rest_framework.routers import DefaultRouter
from users.views import SubscribeView, SubscriptionsView

router_v1 = DefaultRouter()

router_v1.register(r'recipes', RecipesViewSet)
router_v1.register(r'tags', TagsViewSet)
router_v1.register(r'ingredients', IngredientsViewSet)

urlpatterns = [
    path('users/subscriptions/', SubscriptionsView.as_view()),
    path('users/<int:id>/subscribe/', SubscribeView.as_view()),
    path('recipes/<int:id>/favorite/', FavoriteView.as_view()),
    path('recipes/<int:id>/shopping_cart/', ShoppingCartView.as_view()),
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]
