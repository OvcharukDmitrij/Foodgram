from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from djoser.views import UserViewSet
from .serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    """Функция выдачи списка пользователей, конкретного пользователя
    и регистрации пользователя."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberPagination


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login(request):
#     """Функция выдачи JWT токена."""
#
#     serializer = LoginSerializer(data=request.data)
#     if serializer.is_valid():
#         email = serializer.validated_data['email']
#         password = serializer.validated_data['password']
#         user = get_object_or_404(User, email=email)
#         if user.password != password:
#             raise ValidationError('Пароль указан не верно!')
#         refresh = RefreshToken.for_user(user)
#         return Response({"auth_token": f'{str(refresh.access_token)}'},
#                         status=status.HTTP_201_CREATED
#                         )
#
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def logout(request):
#     """Функция удаления JWT токена."""
#
#     user = request.user
#     user.is_anonymous()
#     user.save()
#     return Response('Токен удален!')
#
#
#
#
# class ListRetrieveCreateViewSet(mixins.CreateModelMixin,
#                                 mixins.ListModelMixin,
#                                 mixins.RetrieveModelMixin,
#                                 viewsets.GenericViewSet):
#     """Миксин для модели User."""
#
#     pass


# class UserViewSet(ListRetrieveCreateViewSet):
#     """Функция выдачи списка пользователей, конкретного пользователя
#     и регистрации пользователя."""
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     pagination_class = PageNumberPagination

    # lookup_field = 'id'
    # filter_backends = (filters.SearchFilter, )
    # search_fields = ('id',)
    # permission_classes = (AdminPermission,)
    # http_method_names = ['get', 'post', 'patch', 'delete']
    #

    # def get_serializer_class(self):
    #     if self.action == 'list' or self.action == 'retrieve':
    #         return UserGetSerializer
    #
    #     return UserSerializer
    #
    # @action(
    #     detail=False,
    #     methods=['get'],
    #     url_path='me',
    #     url_name='me',
    #     serializer_class=UserGetSerializer,
    #     permission_classes=(IsAuthenticated,)
    # )
    # def me(self, request):
    #     """Получение данных пользователя."""
    #
    #     serializer = self.get_serializer(request.user)
    #
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    #
    # @action(
    #     detail=False,
    #     methods=['post'],
    #     url_path='set_password',
    #     url_name='set_password',
    #     serializer_class=UserSerializer,
    #     permission_classes=(IsAuthenticated,)
    # )
    # def set_password(self, request):
    #     """Изменение пароля пользователя."""
    #
    #     serializer = SetPasswordSerializer(data=request.data)
    #     user = request.user
    #     if serializer.is_valid():
    #         new_password = serializer.validated_data['new_password']
    #         current_password = serializer.validated_data['current_password']
    #         if user.password != current_password:
    #             raise ValidationError('Текущий пароль указан не верно!')
    #         user.password = new_password
    #         user.save()
    #         return Response('Пароль успешно изменен!',
    #                         status=status.HTTP_204_NO_CONTENT)
    #
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
