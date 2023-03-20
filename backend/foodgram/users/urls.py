from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, login

router_v1 = DefaultRouter()

router_v1.register('', UserViewSet)


urlpatterns = [
    path('token/login/', login),
    # path('token/logout/', ...),
    path('', include(router_v1.urls)),
]