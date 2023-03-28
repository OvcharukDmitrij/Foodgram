from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import RecipesViewSet, IngredientsViewSet, TagsViewSet, FavoriteView # ShopCartViewSet
from users.models import Subscription
from users.views import SubscriptionsViewSet, SubscribeView

router_v1 = DefaultRouter()

router_v1.register(r'recipes', RecipesViewSet, basename='recipes')
router_v1.register(r'users/subscriptions', SubscriptionsViewSet)
router_v1.register(r'tags', TagsViewSet, basename='tags')
router_v1.register(r'ingredients', IngredientsViewSet, basename='ingredients')
# router_v1.register(r'recipes/download_shopping_cart', ShopCartViewSet, basename='favo')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('users/<int:id>/subscribe/', SubscribeView.as_view()),
    path('recipes/<int:id>/favorite/', FavoriteView.as_view())
]
