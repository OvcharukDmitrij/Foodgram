from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router_v1 = DefaultRouter()

router_v1.register(r'recipes', RecipesViewSet)
router_v1.register(r'tags', TagsViewSet)
router_v1.register(r'ingredients', IngredientsViewSet)
router_v1.register(r'users', UsersViewSet)
router_v1.register(r'recipes/(?P<post_id>\d+)/favorite', FavoritViewSet,
                   basename='favorits')
router_v1.register(r'recipes/download_shopping_cart', ShopCartViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
