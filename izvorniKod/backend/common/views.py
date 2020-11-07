from django.contrib import auth
from django.core.mail import send_mail

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework import permissions

from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response


class OnlyFieldsSerializerMixin:
    def get_serializer(self, *args, **kwargs):
        kwargs['only_fields'] = self.only_fields
        return super().get_serializer(*args, **kwargs)


class AccountViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        return UserSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            kwargs['only_fields'] = ['password', 'username', 'first_name', 'last_name', 'email', 'birth_date']
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'confirm' or self.action == 'logout':
            return None
        elif self.action == 'login':
            kwargs['only_fields'] = ['password', 'username']
            return super().get_serializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            send_mail(
                'Potvrda registracije za aplikaciju Terminko!',
                f'Uputite se u praonicu veša s xicom kako bi zaposlenik mogao potvrditi vaš račun!',
                "noreply@somehost.local",
                [user.email]
            )
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'], name='confirm')
    def confirm(self, request, pk=None):
        user = self.get_object()
        if user is not None and not user.is_active:
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['GET'], name='logged_user_data')
    def logged_user_data(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return Response(
                {'user': UserSerializer(user, only_fields=['username', 'first_name', 'last_name', 'email',
                                                           'birth_date']).data},
                status=status.HTTP_200_OK
            )

        return Response(status=status.HTTP_401_UNAUTHORIZED)