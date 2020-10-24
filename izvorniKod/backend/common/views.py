from django.contrib import auth
from django.http import HttpResponseRedirect
import datetime

from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class OnlyFieldsSerializerMixin:
    def get_serializer(self, *args, **kwargs):
        kwargs['only_fields'] = self.only_fields
        return super().get_serializer(*args, **kwargs)


class AccountViewSet(OnlyFieldsSerializerMixin, mixins.CreateModelMixin,viewsets.GenericViewSet):
    serializer_class = UserSerializer
    only_fields = ['password', 'username', 'first_name', 'last_name', 'email', 'birth_date']

    @action(detail=False, methods=['POST'], name='Login')
    def login(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/api/time/")
        else:
            return Response({'error': 'Wrong login data'})

    @action(detail=False, methods=['GET'], name='Logout')
    def logout(self, request, *args, **kwargs):
        auth.logout(request)
        # Redirect to a success page.
        return HttpResponseRedirect("/api/time/")


class TimeView(APIView):

    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        return Response({
            'now': now,
            'user': UserSerializer(request.user, only_fields=['username', 'email']).data
        })
