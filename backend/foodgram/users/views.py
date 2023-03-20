from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from .models import User

from .permissions import AdminPermission
from .serializers import UserSerializer, UserGetSerializer, LoginSerializer, SetPasswordSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Функция выдачи JWT токена."""

    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = get_object_or_404(User, email=email)
        if user.password == password:
            refresh = RefreshToken.for_user(user)
            return Response({"auth_token": f'{str(refresh.access_token)}'},
                            status=status.HTTP_201_CREATED
                            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Функция выдачи списка пользователей, конкретного пользователя
    и регистрации пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    # lookup_field = 'id'
    # filter_backends = (filters.SearchFilter, )
    # search_fields = ('id',)
    # permission_classes = (AdminPermission,)
    # http_method_names = ['get', 'post', 'patch', 'delete']
    #

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return UserGetSerializer

        return UserSerializer


    @action(
        detail=False,
        methods=['get'],
        url_path='me',
        url_name='me',
        serializer_class=UserGetSerializer,
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request):
        """Получение данных пользователя."""

        serializer = self.get_serializer(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['post'],
        url_path='set_password',
        url_name='set_password',
        serializer_class=SetPasswordSerializer,
        permission_classes=(IsAuthenticated, )
    )
    def set_password(self, request):
        """Изменение пароля пользователя."""

        serializer = SetPasswordSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            current_password = serializer.validated_data['current_password']
            new_password = serializer.validated_data['new_password']
            if user.password == current_password:
                user.password = new_password
                user.save()

                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_200_OK)