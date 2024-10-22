from rest_framework.response import Response
from rest_framework import status, generics
from app.models import User, Position, Role
from app.serializers.user import UserSerializer, UserCreateSerializer, UserUpdateSerializer
from django.utils import timezone
from django.views.generic import ListView
from rest_framework.exceptions import PermissionDenied, NotFound
from app.api.login import is_auth



class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    @is_auth({Role.ADMIN.value})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ActiveUserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'


    def get_queryset(self):
        queryset = User.objects.filter(date_terminated__isnull=True).select_related('position')

        position = self.request.GET.get('position', None)
        if position is not None:
            queryset = queryset.filter(position__title__iexact=position)
        return queryset

class ActiveUserJsonView(generics.ListAPIView):
    queryset = User.objects.filter(date_terminated__isnull=True).select_related('position').all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        position = self.request.GET.get('position', None)
        if position:
            queryset = queryset.filter(position__title__iexact=position)
        return queryset

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.select_related('position').all()
    serializer_class = UserSerializer
    lookup_field = 'id'

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'id'

    @is_auth({Role.ADMIN.value, Role.MANAGER.value})
    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserTerminateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    @is_auth({Role.ADMIN.value})
    def delete(self, request, *args, **kwargs):

        user = self.get_object()

        if user.position.rights_level == Role.ADMIN.value:
            raise PermissionDenied("Нельзя удалить пользователя с ролью 'Администратор'.")

        try:
            inactive_position = Position.objects.filter(rights_level=Role.INACTIVE.value).first()
            user.position = inactive_position
        except Position.DoesNotExist:
            raise NotFound("Позиция 'Неактивный сотрудник' не найдена.")

        user.date_terminated = timezone.now()
        user.save()

        return Response({"detail": "Пользователь помечен как неактивный."}, status=status.HTTP_200_OK)
